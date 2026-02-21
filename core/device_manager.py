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

    @property
    def descriptor(self) -> DeviceDescriptor:
        return self._descriptor

    @property
    def connected(self) -> bool:
        return self.status == DeviceStatus.CONNECTED

    def disconnect(self) -> None:
        if self._transport is not None:
            try:
                self._transport.close()
            except Exception:
                pass
        self._transport = None
        self.status = DeviceStatus.DISCONNECTED
        self.last_error = None

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

        except TransportError as e:
            self._transport = None
            self.status = DeviceStatus.ERROR
            # self.last_error = "Transport error"
            self.last_error = str(e)
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

    def set_powersave(self, enabled: bool) -> None:
        if not self.connected or self._transport is None:
            raise RuntimeError("Device not connected")
        from core import protocol
        protocol.write_byte(self._transport, protocol.COMMAND_POWERSAVE, 0, 1 if enabled else 0)


    def set_input_enable(self, idx: int, enabled: bool) -> None:
        if not self.connected or self._transport is None:
            raise RuntimeError("Device not connected")
        from core import protocol
        protocol.write_byte(self._transport, protocol.COMMAND_INPUT_ENABLE, idx, 1 if enabled else 0)


    def set_monitoring_mode(self, idx: int, mode: int) -> None:
        if not self.connected or self._transport is None:
            raise RuntimeError("Device not connected")
        from core import protocol
        protocol.write_byte(self._transport, protocol.COMMAND_MONITORING_MODE, idx, int(mode))


    def set_routing(self, idx: int, route: int) -> None:
        if not self.connected or self._transport is None:
            raise RuntimeError("Device not connected")
        from core import protocol
        protocol.write_byte(self._transport, protocol.COMMAND_ROUTING, idx, int(route))