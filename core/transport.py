# core/transport.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Optional


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
