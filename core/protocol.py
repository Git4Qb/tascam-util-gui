# core/protocol.py

"""US4x4 communication protocol"""

from __future__ import annotations
from core.transport import Transport, CtrlRequest

VENDOR_ID=0x0644
PRODUCT_ID = 0x804e

COMMAND_POWERSAVE = 0x03
COMMAND_INPUT_ENABLE = 0x05
COMMAND_MONITORING_MODE = 0x07
COMMAND_ROUTING = 0x09

INDICES_POWERSAVE = [0]
INDICES_INPUT_ENABLE = [0, 1, 2, 3]
INDICES_MONITORING_MODE = [0, 1]
INDICES_ROUTING = [0, 1]

_PREP_BM = 0xA1
_PREP_B = 2
_PREP_WVALUE = 0x0100
_PREP_WINDEX = 0x2900

_READ_BM = 0xC0


def read_byte(transport: Transport, command: int, index: int) -> int:
    """
    Read a single byte parameter from the device.

    Vendored sequence:
      - prep ctrl_transfer (len 16)
      - prep ctrl_transfer (len 50)
      - read ctrl_transfer (len 1) -> result[0]
    """
    # “handshake” / prepare
    transport.ctrl_transfer_in(CtrlRequest(_PREP_BM, _PREP_B, _PREP_WVALUE, _PREP_WINDEX, 16))
    transport.ctrl_transfer_in(CtrlRequest(_PREP_BM, _PREP_B, _PREP_WVALUE, _PREP_WINDEX, 50))

    # actual read
    data = transport.ctrl_transfer_in(CtrlRequest(_READ_BM, command, 0, index, 1))
    return data[0]
