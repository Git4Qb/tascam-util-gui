# tuxam/tools/usb_inspector.py

import usb
from tuxam.devices.find_device import find_tascam_devices



class UsbInspector:
    def __init__(self, device, device_info):
        self._dev = device
        self.device_info = device_info
        self.interface_number = device_info.control_interface

    def debug_dump_interfaces(self) -> None:
        """Print interface overview (class/subclass/protocol + kernel driver + endpoints)."""
        dev = self._dev
        if dev is None:
            print("no device")
            return

        try:
            cfg = dev.get_active_configuration()
        except usb.USBError as e:
            print(f"[USB] Cannot get active configuration: {e}")
            return

        print("[USB] Interface dump:")
        for intf in cfg:
            num = int(intf.bInterfaceNumber)
            cls = int(intf.bInterfaceClass)
            sub = int(intf.bInterfaceSubClass)
            proto = int(intf.bInterfaceProtocol)

            active = None
            try:
                active = dev.is_kernel_driver_active(num)
            except Exception:
                pass

            print(
                f"  - iface {num}: class=0x{cls:02X} sub=0x{sub:02X} "
                f"proto=0x{proto:02X} kernel_active={active}"
            )
            for ep in intf.endpoints():
                addr = int(ep.bEndpointAddress)
                attr = int(ep.bmAttributes)
                mps = int(ep.wMaxPacketSize)
                print(f"      ep 0x{addr:02X} attr=0x{attr:02X} maxpkt={mps}")

if __name__ == "__main__":
    supported, unsupported = find_tascam_devices()
    if not supported:
        print("No supported Tascam device found")
    else:
        device_object, descriptor = supported[0]
        device_usb = UsbInspector(device_object, descriptor)
        device_usb.debug_dump_interfaces()
