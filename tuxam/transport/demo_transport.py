from __future__ import annotations

from tuxam.devices.us_4x4 import parameters
from tuxam.transport.usb_transport import CtrlRequest, Disconnected


class DemoTransport:
    """In-memory transport for demo mode."""

    def __init__(self) -> None:
        self._open = False
        self._values: dict[tuple[int, int], int] = {}

        for feature in parameters.FEATURES.values():
            for index in feature:
                self._values[(feature.command_read, index)] = 0

    def open(self) -> None:
        self._open = True

    def close(self) -> None:
        self._open = False

    def is_open(self) -> bool:
        return self._open

    def ctrl_transfer_in(self, req: CtrlRequest) -> bytes:
        self._require_open()

        if req.length <= 0:
            return b""

        value = self._values.get((req.b_request, req.w_index), 0)
        return bytes([value]) + (b"\x00" * (req.length - 1))

    def ctrl_transfer_out(self, req: CtrlRequest) -> int:
        self._require_open()

        for feature in parameters.FEATURES.values():
            if feature.command_write == req.b_request:
                self._values[(feature.command_read, req.w_index)] = req.w_value & 0xFF
                break

        return len(req.data)

    def _require_open(self) -> None:
        if not self._open:
            raise Disconnected("DemoTransport is not open")
