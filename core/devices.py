# core/devices.py
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DeviceDescriptor:
    name: str
    vendor_id: int
    product_id: int


""" Supported device descriptors (registry). """
US4X4 = DeviceDescriptor(
    name = "Tascam US-4X4",
    vendor_id = 0x0644,
    product_id = 0x804E
)

# Placeholder until find the real PID for US-4x4HR
US4X4HR = DeviceDescriptor(
    name = "Tascam US-4X4HR",
    vendor_id = 0x0644,
    product_id = 0x0000
)

# Placeholder until find the real PID for US-16x08
US16X08 = DeviceDescriptor(
    name = "Tascam US-16X08",
    vendor_id = 0x0644,
    product_id = 0x0000
)

SUPPORTED_DEVICES: tuple[DeviceDescriptor, ...] = (US4X4, US4X4HR, US16X08)
