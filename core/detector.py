# core/detector.py
from __future__ import annotations

from core.devices import DeviceDescriptor, SUPPORTED_DEVICES
from core.transport import PyUsbTransport


def detect_supported_devices(
    supported: tuple[DeviceDescriptor, ...] = SUPPORTED_DEVICES,
) -> list[DeviceDescriptor]:
    found: list[DeviceDescriptor] = []

    for d in supported:
        if PyUsbTransport.is_present(d.vendor_id, d.product_id):
            found.append(d)

    return found
