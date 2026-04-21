# tuxam/tools/fake_transport.py

# --- Fake transport for tests without device ------------------------------
from tuxam.transport.usb_transport import CtrlRequest, Disconnected

class FakeTransport:
    """
    Inject canned replies keyed by (bm, b, v, i, length).
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