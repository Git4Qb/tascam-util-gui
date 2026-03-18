# tools/driver_registry.py

from tuxam.drivers.US4X4Driver import US4X4Driver

DRIVERS_BY_PRODUCT_ID = {
    0x804E: US4X4Driver,
}