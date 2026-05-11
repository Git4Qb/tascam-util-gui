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
    QStackedWidget,
)

from tuxam.app_mode import AppMode
from tuxam.ui.styles import (
    get_main_window_style,
    get_button_style,
    get_primary_button_style,
    get_status_label_style,
    get_panel_style,
)

from tuxam.devices.demo_device_service import DemoDeviceService
from tuxam.devices.device_service import DeviceService, RealDeviceService
from tuxam.ui.widgets.us4x4_card import US4x4Card
from tuxam.ui.assets.icons.app_icon import get_app_icon
from tuxam.ui.widgets.no_device_view import NoDeviceView
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
        self.scan_error = None

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

        self.center_panel = QFrame()
        self.bottom_panel = QFrame()

        self.center_panel.setStyleSheet(get_panel_style())
        self.bottom_panel.setStyleSheet(get_panel_style())

        center_layout = QVBoxLayout(self.center_panel)
        center_layout.setContentsMargins(0, 0, 0, 18)
        center_layout.setSpacing(12)

        bottom_layout = QVBoxLayout(self.bottom_panel)
        bottom_layout.setContentsMargins(24, 10, 24, 10)

        self.open_button = QPushButton("Open device")
        self.open_button.setStyleSheet(get_primary_button_style())
        self.open_button.setEnabled(False)

        self.rescan_button = QPushButton("Rescan")
        self.rescan_button.setStyleSheet(get_button_style())

        self.mode_button = QPushButton()
        self.mode_button.setStyleSheet(get_button_style())

        self.selector = PenguinSelector()
        self.no_device_view = NoDeviceView()
        self.center_stack = QStackedWidget()
        self.center_stack.addWidget(self.selector)
        self.center_stack.addWidget(self.no_device_view)
        center_layout.addWidget(self.center_stack)

        self.device_actions = QFrame()
        device_actions_layout = QHBoxLayout(self.device_actions)
        device_actions_layout.setContentsMargins(24, 0, 24, 0)
        device_actions_layout.setSpacing(10)
        device_actions_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        device_actions_layout.addWidget(self.open_button)
        device_actions_layout.addWidget(self.rescan_button)
        device_actions_layout.addWidget(self.mode_button)
        center_layout.addWidget(self.device_actions)

        self.status_label = QLabel("Select a device and click Open device")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(get_status_label_style())
        bottom_layout.addWidget(self.status_label)

        main_layout.addWidget(self.center_panel, 1)
        main_layout.addWidget(self.bottom_panel)

        outer_layout.addWidget(self.bg_frame)

    def _connect_signals(self):
        self.rescan_button.clicked.connect(self._on_rescan_clicked)
        self.open_button.clicked.connect(self._on_open_clicked)
        self.mode_button.clicked.connect(self._on_mode_clicked)
        self.selector.device_list.currentRowChanged.connect(self._on_device_selected)
        self.no_device_view.rescan_requested.connect(self._on_rescan_clicked)
        self.no_device_view.demo_mode_requested.connect(self._switch_to_demo_mode)
        self.no_device_view.quit_requested.connect(QApplication.instance().quit)

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
        self._close_open_device()
        self._scan_devices()

    def _scan_devices(self):
        self.driver = None
        self.state = None

        try:
            self.device_options = self.device_service.scan_devices()
            self.scan_error = None
        except Exception as e:
            self.device_options = []
            self.scan_error = e

        self.selector.device_list.clear()

        for option in self.device_options:
            self.selector.device_list.addItem(option.label)

        self.selector.device_list.setCurrentRow(0 if self.selector.device_list.count() else -1)
        self.open_button.setEnabled(False)
        self._update_center_view()

        if self.scan_error is not None:
            self.status_label.setText(f"Device scan failed: {self.scan_error}")
        elif self.device_options:
            self.status_label.setText("Device list updated")
        elif self.app_mode is AppMode.DEMO:
            self.status_label.setText("No demo devices available")
        else:
            self.status_label.setText("No Tascam devices found")

    def _update_center_view(self):
        if self.scan_error is not None:
            self.no_device_view.show_scan_error(self.scan_error)
            self.center_stack.setCurrentWidget(self.no_device_view)
            self.device_actions.setVisible(False)
            return

        if self.device_options:
            self.center_stack.setCurrentWidget(self.selector)
            self.device_actions.setVisible(True)
            return

        if self.app_mode is AppMode.DEMO:
            self.no_device_view.show_no_demo_devices()
        else:
            self.no_device_view.show_real_no_devices()

        self.center_stack.setCurrentWidget(self.no_device_view)
        self.device_actions.setVisible(False)

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

        if self.device_options:
            self.status_label.setText("Real device mode enabled")

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
        self._close_open_device()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
