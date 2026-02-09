import usb.core
import usb.util
import sys

# Find your Tascam US-4x4 device by Vendor and Product ID
VENDOR_ID = 0x0644
PRODUCT_ID = 0x804e
def get_device():
    device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

    if device is None:
        raise ValueError("Device not found")

    # Detach the device from any kernel drivers if needed
    for interface in range(5):  # Assuming there are 5 interfaces
        if device.is_kernel_driver_active(interface):
            device.detach_kernel_driver(interface)

    # Ensure the device is configured
    try:
        device.set_configuration()
        print("Device configured successfully")
    except usb.core.USBError as e:
        print(f"Failed to set configuration: {e}")
        sys.exit(1)

    # Claim the necessary interfaces
    for interface in range(5):
        try:
            usb.util.claim_interface(device, interface)
        except usb.core.USBError as e:
            print(f"Failed to claim interface {interface}: {e}")
            # Clean up before exiting
            for i in range(interface):
                usb.util.release_interface(device, i)
            sys.exit(1)

    # Perform your operations here

    # Release the interfaces if needed
    for interface in range(5):
        usb.util.release_interface(device, interface)

    print("All interfaces released.")
