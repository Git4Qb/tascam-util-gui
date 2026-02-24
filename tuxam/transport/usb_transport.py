# usb_transport.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Optional

import usb.core
import usb.util
import usb  # for usb.USBError


# --- Errors (core-level, no pyusb leaking outside) ----------------------------

class TransportError(RuntimeError):
    """Base transport error."""


class DeviceNotFound(TransportError):
    pass


class PermissionDenied(TransportError):
    pass


class Disconnected(TransportError):
    pass


# --- DTO for control transfer -------------------------------------------------

@dataclass(frozen=True, slots=True)
class CtrlRequest:
    bm_request_type: int
    b_request: int
    w_value: int
    w_index: int
    length: int = 0
    data: bytes = b""
    timeout_ms: int = 1000


# --- Transport interface ------------------------------------------------------

class Transport(Protocol):
    """Minimal contract used by device adapters."""

    def open(self) -> None: ...
    def close(self) -> None: ...
    def is_open(self) -> bool: ...

    def ctrl_transfer_in(self, req: CtrlRequest) -> bytes: ...
    def ctrl_transfer_out(self, req: CtrlRequest) -> int: ...


# --- Fake transport for tests/dev without device ------------------------------

class FakeTransport:
    """
    Simple deterministic fake.
    You can inject canned replies keyed by (bm, b, v, i, length).
    """

    def __init__(self) -> None:
        self._open = False
        self._replies: dict[tuple[int, int, int, int, int], bytes] = {}

    def set_reply(self, *, bm: int, b: int, v: int, i: int, length: int, data: bytes) -> None:
        self._replies[(bm, b, v, i, length)] = data

    def open(self) -> None:
        self._open = True

    def close(self) -> None:
        self._open = False

    def is_open(self) -> bool:
        return self._open

    def ctrl_transfer_in(self, req: CtrlRequest) -> bytes:
        if not self._open:
            raise Disconnected("FakeTransport is not open")

        key = (req.bm_request_type, req.b_request, req.w_value, req.w_index, req.length)
        data = self._replies.get(key, b"\x00" * req.length)
        return data[:req.length]

    def ctrl_transfer_out(self, req: CtrlRequest) -> int:
        if not self._open:
            raise Disconnected("FakeTransport is not open")
        # pretend we wrote all bytes
        return len(req.data)



class PyUsbTransport:
    """
    Real transport backed by PyUSB.
    Owns the device handle and claimed interfaces.

    Strategy:
    - Prefer claiming without detaching kernel drivers.
    - If an interface is busy, detach only that interface and retry claim.
    - Track detached interfaces and optionally reattach on close (best-effort).
    """

    def __init__(self, vendor_id: int, product_id: int) -> None:
        self._vendor_id = vendor_id
        self._product_id = product_id
        self._dev: Optional[usb.core.Device] = None
        self._cfg = None
        self._claimed_ifaces: set[int] = set()
        self._detached_ifaces: set[int] = set()

    @staticmethod
    def is_present(vendor_id: int, product_id: int) -> bool:
        return usb.core.find(idVendor=vendor_id, idProduct=product_id) is not None

    def open(self) -> None:
        dev = usb.core.find(idVendor=self._vendor_id, idProduct=self._product_id)
        if dev is None:
            raise DeviceNotFound("USB device not found")

        try:
            # Best-effort: ensure a configuration is selected.
            # Some backends/devices already have an active configuration.
            try:
                dev.set_configuration()
            except usb.USBError:
                pass

            cfg = dev.get_active_configuration()

            # Try to claim each interface. Detach only if needed.
            for intf in cfg:
                iface_num = intf.bInterfaceNumber

                try:
                    usb.util.claim_interface(dev, iface_num)
                    self._claimed_ifaces.add(iface_num)
                    continue
                except usb.USBError:
                    # Claim failed; try detaching kernel driver and retry claim.
                    try:
                        if dev.is_kernel_driver_active(iface_num):
                            dev.detach_kernel_driver(iface_num)
                            self._detached_ifaces.add(iface_num)
                    except (NotImplementedError, usb.USBError):
                        # Backend doesn't support kernel driver ops or permission issues.
                        pass

                    # Retry claim after detach attempt
                    usb.util.claim_interface(dev, iface_num)
                    self._claimed_ifaces.add(iface_num)

        except usb.USBError as e:
            msg = str(e).lower()
            if "access" in msg or "permission" in msg:
                raise PermissionDenied(str(e)) from e
            raise TransportError(str(e)) from e

        self._dev = dev
        self._cfg = cfg

    def close(self) -> None:
        dev = self._dev
        cfg = self._cfg

        self._dev = None
        self._cfg = None

        if dev is None or cfg is None:
            self._claimed_ifaces.clear()
            self._detached_ifaces.clear()
            return

        try:
            # Release claimed interfaces
            for iface_num in sorted(self._claimed_ifaces):
                try:
                    usb.util.release_interface(dev, iface_num)
                except usb.USBError:
                    pass

            # Optional: reattach only those we detached (best-effort)
            for iface_num in sorted(self._detached_ifaces):
                try:
                    dev.attach_kernel_driver(iface_num)
                except usb.USBError:
                    pass

        finally:
            self._claimed_ifaces.clear()
            self._detached_ifaces.clear()

    def is_open(self) -> bool:
        return self._dev is not None

    def _require_open(self) -> usb.core.Device:
        if self._dev is None:
            raise Disconnected("USB device is not open")
        return self._dev

    def ctrl_transfer_in(self, req: CtrlRequest) -> bytes:
        dev = self._require_open()
        try:
            data = dev.ctrl_transfer(
                req.bm_request_type,
                req.b_request,
                req.w_value,
                req.w_index,
                req.length,
                req.timeout_ms,
            )
            return bytes(data)
        except usb.USBError as e:
            raise TransportError(str(e)) from e

    def ctrl_transfer_out(self, req: CtrlRequest) -> int:
        dev = self._require_open()
        try:
            return dev.ctrl_transfer(
                req.bm_request_type,
                req.b_request,
                req.w_value,
                req.w_index,
                req.data,
                req.timeout_ms,
            )
        except usb.USBError as e:
            raise TransportError(str(e)) from e