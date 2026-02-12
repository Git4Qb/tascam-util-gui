# core/device_state.py

from dataclasses import dataclass

@dataclass
class DeviceState:
    powersave: bool
    input_enable: list[bool]
    monitoring_mode: list[int]
    routing: list[int]