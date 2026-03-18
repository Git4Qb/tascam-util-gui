# tools/test_route_change.py

import usb.core

VENDOR_ID = 0x0644
PRODUCT_ID = 0x804e

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    raise SystemExit("Tascam not found")

print("Device found.")

# # Routing: destination LINE12 (0) takes source PC12 (1)
result = dev.ctrl_transfer(0x40, 10, 0, 0, None)
print("LINE12 takes audio from source:", result)