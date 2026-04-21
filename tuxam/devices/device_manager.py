# devices/device_manager.py

from __future__ import annotations

from tuxam.devices.find_device import find_tascam_devices
from tuxam.drivers.driver_registry import DRIVERS_BY_PRODUCT_ID
from tuxam.transport.usb_transport import PyUsbTransport


def select_driver():
    supported, _ = find_tascam_devices()

    if not supported:
        return None

    dev, descriptor = supported[0]
    pid = dev.idProduct

    driver = DRIVERS_BY_PRODUCT_ID.get(pid)
    if not driver:
        return None

    transport = PyUsbTransport(
        vendor_id=dev.idVendor,
        product_id=dev.idProduct,
        control_interface=descriptor.control_interface,
    )
    transport.open()

    return driver(transport)

# TODO: Change the way supported device is picked