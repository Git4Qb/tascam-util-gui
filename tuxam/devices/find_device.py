# tools/find_device.py

from __future__ import annotations
import usb.core
from tuxam.devices.device_registry import TASCAM_VENDOR_ID, DEVICES_BY_PRODUCT_ID


def devices_plugged_in():

    devices = list(
        usb.core.find(
            find_all=True,
            idVendor = TASCAM_VENDOR_ID
        )
    )
    supported = []
    unsupported = []

    for dev in devices:
        pid = dev.idProduct
        descriptor = DEVICES_BY_PRODUCT_ID.get(pid)

        if descriptor and descriptor.supported:
            supported.append(dev)
        else:
            unsupported.append(dev)
    print(supported, unsupported)
    return supported, unsupported
