# usb_transport.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Optional

import usb.core
import usb.util
import usb  # for usb.USBError

_CONTROL_IFACE_NUM = 4  # US-4x4 control via HID interface

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

    Strategy (US-4x4 safe mode):
    - Prefer claiming only the control interface (HID: iface 4).
    - Do NOT touch audio interfaces (0..3).
    - If iface 4 is busy, detach only iface 4 and retry (best-effort).
    - Track detached interfaces and reattach on close (best-effort).
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
        self._dev = dev

        try:
            # Best-effort: ensure a configuration is selected.
            try:
                dev.set_configuration()
            except usb.USBError:
                pass

            cfg = dev.get_active_configuration()

            # Debug: show what interfaces/endpoints exist and which are kernel-bound
            self._debug_dump_interfaces()

            ctrl_iface = _CONTROL_IFACE_NUM

            # Try to claim ONLY the control interface.
            try:
                usb.util.claim_interface(dev, ctrl_iface)
                self._claimed_ifaces.add(ctrl_iface)
            except usb.USBError as e_claim:
                # Claim failed; try detaching kernel driver ONLY on iface 4 and retry.
                try:
                    if dev.is_kernel_driver_active(ctrl_iface):
                        try:
                            dev.detach_kernel_driver(ctrl_iface)
                            self._detached_ifaces.add(ctrl_iface)
                        except usb.USBError:
                            # detach may fail due to permissions/backend; fall through
                            pass
                except (NotImplementedError, usb.USBError):
                    # Backend doesn't support kernel driver ops or permission issues.
                    pass

                # Retry claim after detach attempt
                try:
                    usb.util.claim_interface(dev, ctrl_iface)
                    self._claimed_ifaces.add(ctrl_iface)
                except usb.USBError as e_retry:
                    # Permission-y errors should map cleanly
                    msg = str(e_retry).lower()
                    if "access" in msg or "permission" in msg:
                        raise PermissionDenied(str(e_retry)) from e_retry
                    # Otherwise bubble as transport error (with original context)
                    raise TransportError(str(e_retry)) from e_retry

        except usb.USBError as e:
            msg = str(e).lower()
            if "access" in msg or "permission" in msg:
                raise PermissionDenied(str(e)) from e
            raise TransportError(str(e)) from e

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

    def _debug_dump_interfaces(self) -> None:
        """Print interface overview (class/subclass/protocol + kernel driver + endpoints)."""
        dev = self._dev
        if dev is None:
            return

        try:
            cfg = dev.get_active_configuration()
        except usb.USBError as e:
            print(f"[USB] Cannot get active configuration: {e}")
            return

        print("[USB] Interface dump:")
        for intf in cfg:
            num = int(intf.bInterfaceNumber)
            cls = int(intf.bInterfaceClass)
            sub = int(intf.bInterfaceSubClass)
            proto = int(intf.bInterfaceProtocol)

            active = None
            try:
                active = dev.is_kernel_driver_active(num)
            except Exception:
                pass

            print(
                f"  - iface {num}: class=0x{cls:02X} sub=0x{sub:02X} "
                f"proto=0x{proto:02X} kernel_active={active}"
            )
            for ep in intf.endpoints():
                addr = int(ep.bEndpointAddress)
                attr = int(ep.bmAttributes)
                mps = int(ep.wMaxPacketSize)
                print(f"      ep 0x{addr:02X} attr=0x{attr:02X} maxpkt={mps}")

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