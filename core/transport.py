# core/transport.py
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
    length: int
    timeout_ms: int = 1000


# --- Transport interface ------------------------------------------------------

class Transport(Protocol):
    """Minimal contract used by DeviceManager/Protocol/read_state."""

    def open(self) -> None: ...
    def close(self) -> None: ...
    def is_open(self) -> bool: ...

    def ctrl_transfer_in(self, req: CtrlRequest) -> bytes: ...
    def ctrl_transfer_out(self, bm_request_type: int, b_request: int,
                          w_value: int, w_index: int, data: bytes,
                          timeout_ms: int = 1000) -> int: ...


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

    def ctrl_transfer_out(self, bm_request_type: int, b_request: int,
                          w_value: int, w_index: int, data: bytes,
                          timeout_ms: int = 1000) -> int:
        if not self._open:
            raise Disconnected("FakeTransport is not open")
        # pretend we wrote all bytes
        return len(data)



class PyUsbTransport:
    """
    Real transport backed by PyUSB.
    Owns the device handle and claimed interfaces.
    """

    def __init__(self, vendor_id: int, product_id: int) -> None:
        self._vendor_id = vendor_id
        self._product_id = product_id
        self._dev: Optional[usb.core.Device] = None
        self._cfg = None
        self._claimed = False

    def open(self) -> None:
        dev = usb.core.find(idVendor=self._vendor_id, idProduct=self._product_id)
        if dev is None:
            raise DeviceNotFound("USB device not found")

        try:
            # Ensure a configuration is selected
            dev.set_configuration()
            cfg = dev.get_active_configuration()

            # Detach kernel drivers (vendored does 0..4)
            for iface in range(0, 5):
                try:
                    if dev.is_kernel_driver_active(iface):
                        dev.detach_kernel_driver(iface)
                except (NotImplementedError, usb.USBError):
                    # Some backends/permissions may not support this check cleanly.
                    pass

            # Claim interfaces 0..4, altsetting 0
            for iface in range(0, 5):
                intf = cfg[(iface, 0)]
                usb.util.claim_interface(dev, intf)

        except usb.USBError as e:
            msg = str(e).lower()
            if "access" in msg or "permission" in msg:
                raise PermissionDenied(str(e)) from e
            raise TransportError(str(e)) from e

        self._dev = dev
        self._cfg = cfg
        self._claimed = True

    def close(self) -> None:
        if not self._dev or not self._cfg:
            self._dev = None
            self._cfg = None
            self._claimed = False
            return

        try:
            if self._claimed:
                for iface in range(0, 5):
                    try:
                        intf = self._cfg[(iface, 0)]
                        usb.util.release_interface(self._dev, intf)
                    except usb.USBError:
                        pass

            # vendored attaches only driver 0; we’ll do the same (safe minimal)
            try:
                self._dev.attach_kernel_driver(0)
            except usb.USBError:
                pass

        finally:
            self._dev = None
            self._cfg = None
            self._claimed = False

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
            # PyUSB returns an array('B')-like; convert to bytes
            return bytes(data)
        except usb.USBError as e:
            raise TransportError(str(e)) from e

    def ctrl_transfer_out(
        self,
        bm_request_type: int,
        b_request: int,
        w_value: int,
        w_index: int,
        data: bytes,
        timeout_ms: int = 1000,
    ) -> int:
        dev = self._require_open()
        try:
            return dev.ctrl_transfer(
                bm_request_type,
                b_request,
                w_value,
                w_index,
                data,
                timeout_ms,
            )
        except usb.USBError as e:
            raise TransportError(str(e)) from e
