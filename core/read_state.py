# core/read_state.py
from __future__ import annotations

from core.device_state import DeviceState
from core.transport import Transport
from core import protocol


def read_state(transport: Transport) -> DeviceState:
    """
    Read current device state from the US-4x4 via Transport.
    Returns a fully-populated DeviceState.
    """
    state = DeviceState()

    # powersave (index 0): 0/1
    ps = protocol.read_byte(transport, protocol.COMMAND_POWERSAVE, 0)
    state.powersave = bool(ps)

    # input enable (indices 0..3): 0/1
    for i in protocol.INDICES_INPUT_ENABLE:
        v = protocol.read_byte(transport, protocol.COMMAND_INPUT_ENABLE, i)
        state.input_enable[i] = bool(v)

    # monitoring mode (indices 0..1): 0=Mono, 1=Stereo
    for i in protocol.INDICES_MONITORING_MODE:
        v = protocol.read_byte(transport, protocol.COMMAND_MONITORING_MODE, i)
        state.monitoring_mode[i] = int(v)

    # routing (indices 0..1): device-defined enum index
    for i in protocol.INDICES_ROUTING:
        v = protocol.read_byte(transport, protocol.COMMAND_ROUTING, i)
        state.routing[i] = int(v)

    return state
