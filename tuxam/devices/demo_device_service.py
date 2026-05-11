from __future__ import annotations

from tuxam.devices.device_registry import DEVICES_BY_PRODUCT_ID
from tuxam.devices.device_service import DeviceOption, format_device_label
from tuxam.drivers.driver_registry import DRIVERS_BY_PRODUCT_ID
from tuxam.transport.demo_transport import DemoTransport


DEMO_PRODUCT_ID = 0x804E


class DemoDeviceService:
    def scan_devices(self) -> list[DeviceOption]:
        descriptor = DEVICES_BY_PRODUCT_ID[DEMO_PRODUCT_ID]
        return [
            DeviceOption(
                label=f"{format_device_label(descriptor.name)} (Demo)",
                is_supported=True,
                descriptor=descriptor,
            )
        ]

    def open_driver(self, option: DeviceOption):
        if not option.is_supported:
            raise ValueError("Device is not supported")

        driver_class = DRIVERS_BY_PRODUCT_ID[DEMO_PRODUCT_ID]
        transport = DemoTransport()
        transport.open()
        return driver_class(transport)
