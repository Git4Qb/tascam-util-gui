# tools/test_route_change.py

import usb.core

VENDOR_ID = 0x0644
PRODUCT_ID = 0x804e

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    raise SystemExit("Tascam not found")

print("Device found.")

out_12 = 0
out_34 = 1

mix = 0
line_12 = 1
line_34 = 2

def change_routing(output, mode):
    output = output
    mode = mode
    result = dev.ctrl_transfer(0x40, 10, mode, output, None)
    print(f'Output {output} is now set to mode {mode}')
    return result


change_routing(out_12, mix)