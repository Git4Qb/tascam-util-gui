from __future__ import annotations

from tuxam.devices.device_service import DeviceOption
from tuxam.transport.usb_transport import CtrlRequest, Disconnected


class FakeTransport:
    """In-memory transport for driver tests."""

    def __init__(self) -> None:
        self._open = False
        self._replies: dict[tuple[int, int, int, int, int], bytes] = {}
        self.in_requests: list[CtrlRequest] = []
        self.out_requests: list[CtrlRequest] = []

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

        self.in_requests.append(req)
        key = (req.bm_request_type, req.b_request, req.w_value, req.w_index, req.length)
        data = self._replies.get(key, b"\x00" * req.length)
        return data[: req.length]

    def ctrl_transfer_out(self, req: CtrlRequest) -> int:
        if not self._open:
            raise Disconnected("FakeTransport is not open")

        self.out_requests.append(req)
        return len(req.data)


class FakeDriver:
    def __init__(self, state: dict | None = None) -> None:
        self.state = state or {}

    def read_device_state(self) -> dict:
        return self.state


class FakeDeviceService:
    def __init__(
        self,
        options: list[DeviceOption] | None = None,
        driver: FakeDriver | None = None,
    ) -> None:
        self.options = options or [
            DeviceOption(label="Fake Tascam US-4x4", is_supported=True)
        ]
        self.driver = driver or FakeDriver()
        self.opened_options: list[DeviceOption] = []

    def scan_devices(self) -> list[DeviceOption]:
        return self.options

    def open_driver(self, option: DeviceOption) -> FakeDriver:
        self.opened_options.append(option)
        return self.driver


class FailingDeviceService:
    def __init__(self, error: Exception | None = None) -> None:
        self.error = error or RuntimeError("USB backend unavailable")

    def scan_devices(self) -> list[DeviceOption]:
        raise self.error

    def open_driver(self, option: DeviceOption) -> FakeDriver:
        raise AssertionError("open_driver should not be called after a failed scan")
