from __future__ import annotations

import unittest

from tuxam.devices.demo_device_service import DemoDeviceService
from tuxam.devices.us_4x4.parameters import INPUT_CHANNEL, InputChannelState


class DemoDeviceServiceTests(unittest.TestCase):
    def test_scan_devices_returns_demo_us4x4(self) -> None:
        service = DemoDeviceService()

        options = service.scan_devices()

        self.assertEqual(len(options), 1)
        self.assertEqual(options[0].label, "US-4X4 (Demo)")
        self.assertTrue(options[0].is_supported)

    def test_open_driver_uses_in_memory_state(self) -> None:
        service = DemoDeviceService()
        option = service.scan_devices()[0]
        driver = service.open_driver(option)

        self.assertIs(driver.read_feature_state(INPUT_CHANNEL, 0), InputChannelState.OFF)

        driver.write_feature_state(INPUT_CHANNEL, InputChannelState.ON, 0)

        self.assertIs(driver.read_feature_state(INPUT_CHANNEL, 0), InputChannelState.ON)


if __name__ == "__main__":
    unittest.main()
