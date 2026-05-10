from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from tuxam.devices.device_registry import DeviceInfo
from tuxam.devices.find_device import find_tascam_devices
from tuxam.drivers.driver_registry import DRIVERS_BY_PRODUCT_ID
from tuxam.transport.usb_transport import PyUsbTransport


@dataclass(frozen=True, slots=True)
class DeviceOption:
    label: str
    is_supported: bool
    device: object | None = None
    descriptor: DeviceInfo | None = None


class DeviceService(Protocol):
    def scan_devices(self) -> list[DeviceOption]: ...
    def open_driver(self, option: DeviceOption): ...


class RealDeviceService:
    def __init__(self, device_finder=find_tascam_devices):
        self._device_finder = device_finder

    def scan_devices(self) -> list[DeviceOption]:
        supported, unsupported = self._device_finder()
        options = []

        for dev, desc in supported:
            options.append(
                DeviceOption(
                    label=desc.name,
                    is_supported=True,
                    device=dev,
                    descriptor=desc,
                )
            )

        for dev, desc in unsupported:
            name = desc.name if desc else "Unknown Tascam device"
            options.append(
                DeviceOption(
                    label=f"{name} (Unsupported device)",
                    is_supported=False,
                    device=dev,
                    descriptor=desc,
                )
            )

        return options

    def open_driver(self, option: DeviceOption):
        if not option.is_supported:
            raise ValueError("Device is not supported")

        if option.device is None or option.descriptor is None:
            raise ValueError("Selected device is incomplete")

        product_id = option.device.idProduct
        driver_class = DRIVERS_BY_PRODUCT_ID.get(product_id)
        if driver_class is None:
            raise ValueError("No driver registered for selected device")

        control_interface = option.descriptor.control_interface
        if control_interface is None:
            raise ValueError("Selected device has no control interface")

        transport = PyUsbTransport(
            vendor_id=option.device.idVendor,
            product_id=product_id,
            control_interface=control_interface,
        )
        transport.open()

        return driver_class(transport)
