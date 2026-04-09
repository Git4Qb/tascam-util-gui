# devices/device_registry.py


from __future__ import annotations
from dataclasses import dataclass

TASCAM_VENDOR_ID = 0x0644

@dataclass(frozen=True, slots=True)
class DeviceID:
    name: str
    product_id: int | None
    supported: bool

DEVICES = (
    DeviceID(
        name="Tascam US-4X4",
        product_id=0x804E,
        supported=True
    ),
    DeviceID(
        name="Tascam US-2X2HR",
        product_id=None,
        supported=False
    ),
    DeviceID(
        name="Tascam US-4X4HR",
        product_id=None,
        supported=False
    ),
    DeviceID(
        name="Tascam US-16X08",
        product_id=None,
        supported=False
    )
)

SUPPORTED_DEVICES = tuple(d for d in DEVICES if d.supported)
PLANNED_DEVICES = tuple(d for d in DEVICES if not d.supported)

DEVICES_BY_PRODUCT_ID = {
    d.product_id: d
    for d in DEVICES
    if d.product_id is not None
}