from __future__ import annotations

import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from tuxam.app_mode import AppMode
from tuxam.devices.device_service import DeviceOption
from tuxam.ui.main_window import MainWindow


class ClosableTransport:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


class ReadFailingDriver:
    def __init__(self) -> None:
        self.transport = ClosableTransport()

    def read_device_state(self) -> dict:
        raise RuntimeError("state read failed")


class OpenableDriver:
    def __init__(self) -> None:
        self.transport = ClosableTransport()

    def read_device_state(self) -> dict:
        return {}


class ReadFailingDeviceService:
    def __init__(self, driver=None) -> None:
        self.driver = driver or ReadFailingDriver()
        self.option = DeviceOption(label="Fake Tascam US-4x4", is_supported=True)

    def scan_devices(self) -> list[DeviceOption]:
        return [self.option]

    def open_driver(self, option: DeviceOption) -> ReadFailingDriver:
        return self.driver


class OpenFailureMainWindow(MainWindow):
    def __init__(self, device_service: ReadFailingDeviceService):
        self._test_device_service = device_service
        super().__init__(AppMode.REAL)

    def _create_device_service(self, app_mode: AppMode):
        return self._test_device_service


class MainWindowOpenFailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_open_failure_closes_partially_opened_driver_transport(self) -> None:
        service = ReadFailingDeviceService()
        window = OpenFailureMainWindow(service)

        try:
            window._scan_devices()
            window.selector.device_list.setCurrentRow(0)

            window._on_open_clicked()

            self.assertTrue(service.driver.transport.closed)
            self.assertIsNone(window.driver)
            self.assertIsNone(window.state)
            self.assertIsNone(window.card)
            self.assertEqual(window.status_label.text(), "Open failed: state read failed")
        finally:
            window.close()

    def test_closing_card_closes_open_driver_transport(self) -> None:
        driver = OpenableDriver()
        service = ReadFailingDeviceService(driver)
        window = OpenFailureMainWindow(service)

        try:
            window._scan_devices()
            window.selector.device_list.setCurrentRow(0)
            window._on_open_clicked()

            self.assertIs(window.driver, driver)
            self.assertIsNotNone(window.card)

            window.card.close()

            self.assertTrue(driver.transport.closed)
            self.assertIsNone(window.driver)
            self.assertIsNone(window.state)
            self.assertIsNone(window.card)
            self.assertEqual(window.status_label.text(), "Device panel closed")
        finally:
            window.close()


if __name__ == "__main__":
    unittest.main()
