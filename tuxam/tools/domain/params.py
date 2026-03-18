# tuxam/devices/us_4x4/params.py

from enum import IntEnum
from dataclasses import dataclass


class PowerSaveState(IntEnum):
    OFF = 0
    ON = 1


class InputChannelState(IntEnum):
    OFF = 0
    ON = 1


class MonitoringState(IntEnum):
    MONO = 0
    STEREO = 1


class RoutingState(IntEnum):
    MONITOR_MIX = 0
    LINE_1_2 = 1
    LINE_3_4 = 2


@dataclass(frozen=True, slots=True)
class DeviceParameters:
    count: int
    possible_states: type[IntEnum]
    command_read: int
    command_write: int

    def __iter__(self):
        return iter(range(self.count))


powersave = DeviceParameters(
    count=1,
    possible_states=PowerSaveState,
    command_read=0x03,
    command_write=0x04,
)

input_channel = DeviceParameters(
    count=4,
    possible_states=InputChannelState,
    command_read=0x05,
    command_write=0x06,
)

monitoring = DeviceParameters(
    count=2,
    possible_states=MonitoringState,
    command_read=0x07,
    command_write=0x08,
)

routing = DeviceParameters(
    count=2,
    possible_states=RoutingState,
    command_read=0x09,
    command_write=0x10,
)