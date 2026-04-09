#!/usr/bin/env python3

# tools/test_monitor_change.py

import usb.core

VENDOR_ID = 0x0644
PRODUCT_ID = 0x804e

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    raise SystemExit("Tascam not found")

print("Device found.")

# Change monitor mode of IN1 and IN2 (MONO/STEREO)
result = dev.ctrl_transfer(0x40, 8, 0, 0)
print("IN12 are set to MONO:", result)