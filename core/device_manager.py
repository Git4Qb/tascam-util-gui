# core/device_manager.py
from __future__ import annotations

from enum import Enum, auto

from core.devices import DeviceDescriptor
from core.device_state import DeviceState
from core.read_state import read_state as _read_state
from core.transport import (
    PyUsbTransport,
    DeviceNotFound,
    PermissionDenied,
    TransportError,
)


class DeviceStatus(Enum):
    DISCONNECTED = auto()
    CONNECTED = auto()
    ERROR = auto()


class DeviceManager:
    def __init__(self, descriptor: DeviceDescriptor) -> None:
        self._descriptor = descriptor
        self._transport: PyUsbTransport | None = None
        self.last_error: str | None = None
        self.status: DeviceStatus = DeviceStatus.DISCONNECTED

    def connect(self) -> bool:
        self._transport = PyUsbTransport(
            self._descriptor.vendor_id,
            self._descriptor.product_id,
        )

        try:
            self._transport.open()
            self.last_error = None
            self.status = DeviceStatus.CONNECTED
            return True

        except DeviceNotFound:
            self._transport = None
            self.status = DeviceStatus.DISCONNECTED
            self.last_error = "Device not found"
            return False

        except PermissionDenied:
            self._transport = None
            self.status = DeviceStatus.ERROR
            self.last_error = "Permission denied"
            return False

        except TransportError:
            self._transport = None
            self.status = DeviceStatus.ERROR
            self.last_error = "Transport error"
            return False

    def read_state(self) -> DeviceState | None:
        if self.status != DeviceStatus.CONNECTED or self._transport is None:
            return None

        try:
            return _read_state(self._transport)

        except TransportError:
            self._transport = None
            self.status = DeviceStatus.ERROR
            self.last_error = "Communication failed during read"
            return None
