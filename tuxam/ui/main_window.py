# ui/main_window.py

import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox,
)

from tuxam.app_mode import AppMode
from tuxam.ui.styles import (
    get_main_window_style,
    get_button_style,
    get_status_label_style,
    get_panel_style,
)

from tuxam.devices.demo_device_service import DemoDeviceService
from tuxam.devices.device_service import DeviceService, RealDeviceService
from tuxam.ui.widgets.us4x4_card import US4x4Card
from tuxam.ui.assets.icons.app_icon import get_app_icon
from tuxam.ui.widgets.penguin_selector import PenguinSelector


class MainWindow(QWidget):
    def __init__(self, app_mode: AppMode = AppMode.REAL):
        super().__init__()
        self.app_mode = app_mode
        self.device_service = self._create_device_service(app_mode)
        self.driver = None
        self.state = None
        self.card = None
        self.device_options = []
        self.no_devices_dialog = None

        self.setWindowTitle("Tuxam")
        self.resize(640, 640)
        self.setWindowIcon(get_app_icon())
        self.setStyleSheet(get_main_window_style())

        self._build_ui()
        self._update_mode_ui()
        self._connect_signals()
        self._on_device_selected(self.selector.device_list.currentRow())
        QTimer.singleShot(0, self._handle_startup_scan)

    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(20, 20, 20, 20)

        self.bg_frame = QFrame()

        main_layout = QVBoxLayout(self.bg_frame)
        main_layout.setSpacing(15)

        self.top_panel = QFrame()
        self.center_panel = QFrame()
        self.bottom_panel = QFrame()

        self.top_panel.setStyleSheet(get_panel_style())
        self.center_panel.setStyleSheet(get_panel_style())
        self.bottom_panel.setStyleSheet(get_panel_style())

        top_layout = QHBoxLayout(self.top_panel)
        top_layout.setContentsMargins(24, 16, 24, 16)
        top_layout.setSpacing(10)

        center_layout = QVBoxLayout(self.center_panel)
        center_layout.setContentsMargins(0, 0, 0, 0)

        bottom_layout = QVBoxLayout(self.bottom_panel)
        bottom_layout.setContentsMargins(24, 10, 24, 10)

        self.open_button = QPushButton("Open device")
        self.open_button.setStyleSheet(get_button_style())
        self.open_button.setEnabled(False)

        self.rescan_button = QPushButton("Rescan")
        self.rescan_button.setStyleSheet(get_button_style())

        self.mode_button = QPushButton()
        self.mode_button.setStyleSheet(get_button_style())

        top_layout.addWidget(self.rescan_button)
        top_layout.addWidget(self.open_button)
        top_layout.addWidget(self.mode_button)

        self.selector = PenguinSelector()
        center_layout.addWidget(self.selector)

        self.status_label = QLabel("Select a device and click Open device")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(get_status_label_style())
        bottom_layout.addWidget(self.status_label)

        main_layout.addWidget(self.top_panel)
        main_layout.addWidget(self.center_panel, 1)
        main_layout.addWidget(self.bottom_panel)

        outer_layout.addWidget(self.bg_frame)

    def _connect_signals(self):
        self.rescan_button.clicked.connect(self._on_rescan_clicked)
        self.open_button.clicked.connect(self._on_open_clicked)
        self.mode_button.clicked.connect(self._on_mode_clicked)
        self.selector.device_list.currentRowChanged.connect(self._on_device_selected)

    def _create_device_service(self, app_mode: AppMode) -> DeviceService:
        if app_mode is AppMode.DEMO:
            return DemoDeviceService()
        return RealDeviceService()

    def _update_mode_ui(self):
        if self.app_mode is AppMode.DEMO:
            self.mode_button.setText("Real devices")
            return

        self.mode_button.setText("Demo mode")

    def _handle_startup_scan(self):
        self._scan_devices()

        if self.app_mode is AppMode.REAL and not self.device_options:
            self._prompt_no_real_devices_at_startup()

    def _on_device_selected(self, index: int):
        if self.card is not None:
            self.open_button.setEnabled(False)
            self.status_label.setText("Close device panel before opening another device")
            return

        if index < 0 or index >= len(self.device_options):
            self.open_button.setEnabled(False)
            self.status_label.setText("Select a device and click Open device")
            return

        option = self.device_options[index]
        if not option.is_supported:
            self.open_button.setEnabled(False)
            self.status_label.setText("This device is not supported yet")
            return

        self.open_button.setEnabled(True)
        self.status_label.setText("Supported device selected")

    def _on_rescan_clicked(self):
        self._scan_devices()

    def _scan_devices(self):
        self.driver = None
        self.state = None

        try:
            self.device_options = self.device_service.scan_devices()
        except Exception as e:
            self.device_options = []
            self.status_label.setText(f"Device scan failed: {e}")

        self.selector.device_list.clear()

        for option in self.device_options:
            self.selector.device_list.addItem(option.label)

        if not self.device_options:
            self.selector.device_list.addItem("No Tascam devices found")

        self.selector.device_list.setCurrentRow(0 if self.selector.device_list.count() else -1)
        self.open_button.setEnabled(False)

        if self.device_options:
            self.status_label.setText("Device list updated")
        elif self.app_mode is AppMode.DEMO:
            self.status_label.setText("No demo devices available")
        else:
            self.status_label.setText("No Tascam devices found")

    def _on_open_clicked(self):
        if self.card is not None:
            self.status_label.setText("Device panel is already open")
            return

        index = self.selector.device_list.currentRow()
        if index < 0 or index >= len(self.device_options):
            self.status_label.setText("Select a supported device first")
            return

        try:
            option = self.device_options[index]
            self.driver = self.device_service.open_driver(option)
            self.state = self.driver.read_device_state()

            self.card = US4x4Card(self.driver, self.state)
            self.card.closed.connect(self._on_card_closed)
            self.card.show()

            self.open_button.setEnabled(False)
            self.status_label.setText(f"{option.label} opened")

        except Exception as e:
            self.driver = None
            self.state = None
            self.card = None
            self.status_label.setText(f"Open failed: {e}")

    def _on_mode_clicked(self):
        if self.app_mode is AppMode.REAL:
            self._switch_to_demo_mode()
            return

        self._switch_to_real_mode()

    def _switch_to_demo_mode(self):
        if self.driver is not None:
            result = QMessageBox.question(
                self,
                "Switch to Demo Mode",
                "Changes made to your connected device have already been applied.\n"
                "Demo mode will disconnect from the real device and open simulated devices instead.\n"
                "Continue?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if result != QMessageBox.StandardButton.Yes:
                return

        self._close_open_device()
        self.app_mode = AppMode.DEMO
        self.device_service = self._create_device_service(self.app_mode)
        self._update_mode_ui()
        self._scan_devices()
        self.status_label.setText("Demo mode enabled")

    def _switch_to_real_mode(self):
        self._close_open_device()
        self.app_mode = AppMode.REAL
        self.device_service = self._create_device_service(self.app_mode)
        self._update_mode_ui()
        self._scan_devices()

        if not self.device_options:
            self._prompt_no_real_devices_from_demo_mode()
        else:
            self.status_label.setText("Real device mode enabled")

    def _prompt_no_real_devices_at_startup(self):
        self._show_no_devices_dialog(
            [
                ("Demo Mode", self._switch_to_demo_mode),
                ("Rescan", self._rescan_real_devices_from_startup_dialog),
                ("Quit", QApplication.instance().quit),
            ]
        )

    def _prompt_no_real_devices_from_demo_mode(self):
        self._show_no_devices_dialog(
            [
                ("Rescan", self._rescan_real_devices_from_demo_dialog),
                ("Stay in Demo Mode", self._switch_to_demo_mode),
                ("Quit", QApplication.instance().quit),
            ]
        )

    def _show_no_devices_dialog(self, actions):
        if self.no_devices_dialog is not None:
            self.no_devices_dialog.raise_()
            self.no_devices_dialog.activateWindow()
            return

        dialog = QMessageBox(self)
        dialog.setWindowTitle("No Devices Found")
        dialog.setText("No Tascam devices were found.")
        dialog.setModal(False)

        button_actions = {}
        for label, callback in actions:
            button = dialog.addButton(label, QMessageBox.ButtonRole.ActionRole)
            button_actions[button] = callback

        def handle_button(button):
            callback = button_actions.get(button)
            dialog.close()
            if callback is not None:
                callback()

        def clear_dialog():
            if self.no_devices_dialog is dialog:
                self.no_devices_dialog = None

        dialog.buttonClicked.connect(handle_button)
        dialog.finished.connect(clear_dialog)

        self.no_devices_dialog = dialog
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def _rescan_real_devices_from_startup_dialog(self):
        self._scan_devices()

        if self.app_mode is AppMode.REAL and not self.device_options:
            self._prompt_no_real_devices_at_startup()

    def _rescan_real_devices_from_demo_dialog(self):
        self._scan_devices()

        if self.app_mode is AppMode.REAL and not self.device_options:
            self._prompt_no_real_devices_from_demo_mode()

    def _close_open_device(self):
        if self.card is not None:
            self.card.close()
            self.card = None

        if self.driver is not None:
            transport = getattr(self.driver, "transport", None)
            if transport is not None:
                transport.close()

        self.driver = None
        self.state = None

    def _ensure_driver(self):
        if self.driver is None:
            self.status_label.setText("Device not opened")
            return False
        return True

    def _on_card_closed(self):
        self.card = None
        self._on_device_selected(self.selector.device_list.currentRow())
        self.status_label.setText("Device panel closed")

    def closeEvent(self, event):
        if self.no_devices_dialog is not None:
            self.no_devices_dialog.close()
            self.no_devices_dialog = None

        self._close_open_device()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
