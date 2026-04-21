# tuxam/transport/usb_transport.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol
import usb.core
import usb.util
import usb


class TransportError(RuntimeError):
    """Base transport error."""


class DeviceNotFound(TransportError):
    pass


class PermissionDenied(TransportError):
    pass


class Disconnected(TransportError):
    pass


class InterfaceBusy(TransportError):
    """Control interface is already owned by kernel or another driver/process."""
    pass


@dataclass(frozen=True, slots=True)
class CtrlRequest:
    bm_request_type: int
    b_request: int
    w_value: int
    w_index: int
    length: int = 0
    data: bytes = b""
    timeout_ms: int = 1000


class Transport(Protocol):
    def open(self) -> None: ...
    def close(self) -> None: ...
    def is_open(self) -> bool: ...
    def ctrl_transfer_in(self, req: CtrlRequest) -> bytes: ...
    def ctrl_transfer_out(self, req: CtrlRequest) -> int: ...


class PyUsbTransport:
    """
    Transport backed by PyUSB.

    This version NEVER detaches the kernel driver.
    If the control interface cannot be claimed safely, it fails.
    """

    def __init__(self, vendor_id: int, product_id: int, control_interface: int) -> None:
        self._vendor_id = vendor_id
        self._product_id = product_id
        self._control_interface = control_interface
        self._dev: usb.core.Device | None = None
        self._claimed_iface: int | None = None

    @staticmethod
    def is_present(vendor_id: int, product_id: int) -> bool:
        return usb.core.find(idVendor=vendor_id, idProduct=product_id) is not None

    def open(self) -> None:
        dev = usb.core.find(idVendor=self._vendor_id, idProduct=self._product_id)
        if dev is None:
            raise DeviceNotFound("USB device not found")

        try:
            try:
                dev.set_configuration()
            except usb.USBError:
                pass

            ctrl_iface = self._control_interface

            try:
                kernel_active = dev.is_kernel_driver_active(ctrl_iface)
            except (NotImplementedError, usb.USBError):
                kernel_active = False

            if kernel_active:
                raise InterfaceBusy(
                    f"Interface {ctrl_iface} is owned by kernel driver; refusing to detach"
                )

            try:
                usb.util.claim_interface(dev, ctrl_iface)
            except usb.USBError as e:
                msg = str(e).lower()

                if "access" in msg or "permission" in msg:
                    raise PermissionDenied(str(e)) from e

                raise InterfaceBusy(
                    f"Could not claim interface {ctrl_iface} without detaching kernel driver: {e}"
                ) from e

            self._dev = dev
            self._claimed_iface = ctrl_iface

        except (DeviceNotFound, PermissionDenied, InterfaceBusy):
            self._dev = None
            self._claimed_iface = None
            raise

        except usb.USBError as e:
            self._dev = None
            self._claimed_iface = None
            msg = str(e).lower()
            if "access" in msg or "permission" in msg:
                raise PermissionDenied(str(e)) from e
            raise TransportError(str(e)) from e

    def close(self) -> None:
        dev = self._dev
        claimed_iface = self._claimed_iface

        self._dev = None
        self._claimed_iface = None

        if dev is None:
            return

        if claimed_iface is not None:
            try:
                usb.util.release_interface(dev, claimed_iface)
            except usb.USBError:
                pass

    def is_open(self) -> bool:
        return self._dev is not None

    def _require_open(self) -> usb.core.Device:
        if self._dev is None:
            raise Disconnected("USB device is not open")
        return self._dev

    def _ctrl_transfer(self, req: CtrlRequest, payload: int | bytes) -> int | bytes:
        dev = self._require_open()
        try:
            return dev.ctrl_transfer(
                req.bm_request_type,
                req.b_request,
                req.w_value,
                req.w_index,
                payload,
                req.timeout_ms,
            )
        except usb.USBError as e:
            raise TransportError(str(e)) from e

    def ctrl_transfer_in(self, req: CtrlRequest) -> bytes:
        data = self._ctrl_transfer(req, req.length)
        return bytes(data)

    def ctrl_transfer_out(self, req: CtrlRequest) -> int:
        return self._ctrl_transfer(req, req.data)