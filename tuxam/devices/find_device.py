# devices/find_device.py

from __future__ import annotations
import usb.core
from tuxam.devices.device_registry import TASCAM_VENDOR_ID, DEVICES_BY_PRODUCT_ID


def find_tascam_devices():

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
            supported.append((dev, descriptor))
        else:
            unsupported.append(dev)


    return supported, unsupported


