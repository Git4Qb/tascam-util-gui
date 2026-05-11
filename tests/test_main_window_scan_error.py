from __future__ import annotations

import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from tests.fakes import FailingDeviceService
from tuxam.app_mode import AppMode
from tuxam.ui.main_window import MainWindow


class FailingScanMainWindow(MainWindow):
    def __init__(self, device_service: FailingDeviceService):
        self._test_device_service = device_service
        super().__init__(AppMode.REAL)

    def _create_device_service(self, app_mode: AppMode):
        return self._test_device_service


class MainWindowScanErrorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_scan_error_uses_scan_error_empty_state(self) -> None:
        window = FailingScanMainWindow(
            FailingDeviceService(RuntimeError("USB backend unavailable"))
        )

        try:
            window._scan_devices()

            self.assertEqual(window.device_options, [])
            self.assertIsInstance(window.scan_error, RuntimeError)
            self.assertIs(window.center_stack.currentWidget(), window.no_device_view)
            self.assertTrue(window.device_actions.isHidden())
            self.assertEqual(window.no_device_view.title_label.text(), "Device scan failed")
            self.assertEqual(window.no_device_view.rescan_button.text(), "Try Again")
            self.assertIn("USB backend unavailable", window.no_device_view.detail_label.text())
            self.assertFalse(window.no_device_view.demo_button.isHidden())
        finally:
            window.close()


if __name__ == "__main__":
    unittest.main()
