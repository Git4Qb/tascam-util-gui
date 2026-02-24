# device_parameters.py

from enum import IntEnum

class InputChannel(IntEnum):
    IN1 = 0
    IN2 = 1
    IN3 = 2
    IN4 = 3


class RoutingDest(IntEnum):
    LINE12 = 0
    LINE34 = 1


class RoutingSource(IntEnum):
    MONITOR_MIX = 0
    PC_12 = 1
    PC_34 = 2


class MonitoringPair(IntEnum):
    IN12 = 0
    IN34 = 1


class MonitoringMode(IntEnum):
    MONO = 0
    STEREO = 1