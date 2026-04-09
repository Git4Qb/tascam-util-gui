# drivers/driver_registry.py

from tuxam.drivers.us4x4_driver import US4X4Driver

DRIVERS_BY_PRODUCT_ID = {
    0x804E: US4X4Driver,
}