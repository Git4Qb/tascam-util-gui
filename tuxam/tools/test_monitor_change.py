#!/usr/bin/env python3

# tools/test_monitor_change.py

import usb.core

VENDOR_ID = 0x0644
PRODUCT_ID = 0x804e

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    raise SystemExit("Tascam not found")

print("Device found.")

mono = 0
stereo = 1
in12 = 0
in34 = 1

def change_monitor(input_pair, mode):
    input_pair = input_pair
    mode = mode
    result = dev.ctrl_transfer(0x40, 8, mode, input_pair)
    print(f'Inputs {input_pair} is now set to {mode}')
    return result

change_monitor(in12, mono)