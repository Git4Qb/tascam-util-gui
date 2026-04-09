#!/usr/bin/env python3
# tools/test_IN2_enable.py

import usb.core

VENDOR_ID = 0x0644
PRODUCT_ID = 0x804e

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    raise SystemExit("Tascam not found")

print("Device found.")

# Enabling / disabling IN2
result = dev.ctrl_transfer(0x40, 6, 0, 3)
print("IN4 is disabled", result)