# core/device_state.py
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DeviceState:
    # Device defaults (safe baseline until real read happens)
    powersave: bool = False

    # 4 inputs: IN1..IN4
    input_enable: list[bool] = field(default_factory=lambda: [False, False, False, False])

    # 2 monitoring groups: IN1/2 and IN3/4
    # 0=Mono, 1=Stereo (for now; we can replace with Enum later)
    monitoring_mode: list[int] = field(default_factory=lambda: [0, 0])

    # 2 routing groups: Line 1/2 and Line 3/4
    # values are device-defined (for now int; Enum later)
    routing: list[int] = field(default_factory=lambda: [0, 0])
