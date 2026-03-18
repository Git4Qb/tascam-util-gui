# tools/device_manager.py


from __future__ import annotations
from tuxam.devices.find_device import devices_plugged_in
from tuxam.drivers.driver_registry import DRIVERS_BY_PRODUCT_ID


def select_driver():

    supported, _ = devices_plugged_in()

    if not supported:
        return None

    dev = supported[0]
    pid = dev.idProduct
    driver = DRIVERS_BY_PRODUCT_ID.get(pid)
    if driver:
        return driver(dev)

    return None
