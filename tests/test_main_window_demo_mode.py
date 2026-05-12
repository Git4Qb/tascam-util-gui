from __future__ import annotations

import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from tuxam.app_mode import AppMode
from tuxam.ui.main_window import MainWindow


class MainWindowDemoModeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_demo_mode_shows_notice_without_auto_selecting_device(self) -> None:
        window = MainWindow(AppMode.DEMO)

        try:
            window._scan_devices()

            self.assertFalse(window.demo_notice_label.isHidden())
            self.assertIn("simulated device", window.demo_notice_label.text())
            self.assertEqual(window.mode_button.text(), "Real devices")
            self.assertEqual(window.selector.device_list.currentRow(), -1)
            self.assertFalse(window.open_button.isEnabled())
            self.assertEqual(window.status_label.text(), "Select a device and click Open device")
        finally:
            window.close()

    def test_startup_scan_does_not_auto_select_device(self) -> None:
        window = MainWindow(AppMode.DEMO)

        try:
            self.app.processEvents()

            self.assertEqual(window.selector.device_list.currentRow(), -1)
            self.assertIsNone(window.selected_device_index)
            self.assertFalse(window.open_button.isEnabled())
            self.assertEqual(window.status_label.text(), "Select a device and click Open device")
        finally:
            window.close()

    def test_row_selection_enables_open_action(self) -> None:
        window = MainWindow(AppMode.DEMO)

        try:
            window._scan_devices()

            window.selector.device_list.setCurrentRow(0)

            self.assertEqual(window.selected_device_index, 0)
            self.assertTrue(window.open_button.isEnabled())
            self.assertEqual(window.status_label.text(), "Simulated device selected")
        finally:
            window.close()

    def test_real_mode_hides_demo_notice(self) -> None:
        window = MainWindow(AppMode.REAL)

        try:
            window._scan_devices()

            self.assertTrue(window.demo_notice_label.isHidden())
            self.assertEqual(window.mode_button.text(), "Demo mode")
        finally:
            window.close()

    def test_selecting_demo_device_enables_open_action(self) -> None:
        window = MainWindow(AppMode.DEMO)

        try:
            window._scan_devices()

            window.selector.device_list.setCurrentRow(0)

            self.assertEqual(window.selected_device_index, 0)
            self.assertEqual(window.selector.device_list.currentRow(), 0)
            self.assertTrue(window.open_button.isEnabled())
            self.assertEqual(window.status_label.text(), "Simulated device selected")
        finally:
            window.close()

    def test_open_selected_demo_device_shows_device_panel(self) -> None:
        window = MainWindow(AppMode.DEMO)

        try:
            window._scan_devices()
            window.selector.device_list.setCurrentRow(0)

            window._on_open_clicked()

            self.assertIsNotNone(window.driver)
            self.assertIsNotNone(window.card)
            self.assertEqual(window.status_label.text(), "US-4X4 (Demo) opened")
        finally:
            window.close()


if __name__ == "__main__":
    unittest.main()
