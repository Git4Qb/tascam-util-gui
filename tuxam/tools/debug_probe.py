# tuxam/debug_probe.py

from transport.usb_transport import PyUsbTransport

if __name__ == "__main__":
    from tuxam.domain.device_registry import US4X4

    transport = PyUsbTransport(
        vendor_id=US4X4.vendor_id,
        product_id=US4X4.product_id,
    )

    try:
        print("Opening device...")
        transport.open()
        print("Device opened successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        transport.close()
        print("Closed.")