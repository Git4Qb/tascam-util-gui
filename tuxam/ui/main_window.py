# ui/main_window.py

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
)

from tuxam.ui.styles import (
    get_main_window_style,
    get_button_style,
    get_status_label_style,
    # get_background_frame_style,
    get_panel_style,
)

from tuxam.drivers.us4x4_driver import US4X4Driver
from tuxam.tools.fake_transport import FakeTransport
from tuxam.ui.widgets.us4x4_card import US4x4Card
from tuxam.devices.find_device import find_tascam_devices
from tuxam.ui.assets.icons.app_icon import get_app_icon
from tuxam.ui.widgets.penguin_selector import PenguinSelector

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.driver = None
        self.state = None
        self.card = None
        self.supported_devices = []
        self.unsupported_devices = []

        self.setWindowTitle("Tuxam")
        self.resize(560, 640)
        self.setWindowIcon(get_app_icon())
        self.setStyleSheet(get_main_window_style())

        self._build_ui()
        self._connect_signals()
        self._on_device_selected(self.selector.dropdown.currentIndex())
        self._on_rescan_clicked()

    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(20, 20, 20, 20)

        self.bg_frame = QFrame()
        # self.bg_frame.setStyleSheet(get_background_frame_style())

        main_layout = QVBoxLayout(self.bg_frame)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        # --- section frames ---
        self.top_panel = QFrame()
        self.center_panel = QFrame()
        self.bottom_panel = QFrame()

        self.top_panel.setStyleSheet(get_panel_style())
        self.center_panel.setStyleSheet(get_panel_style())
        self.bottom_panel.setStyleSheet(get_panel_style())

        # --- layouts inside panels ---
        top_layout = QHBoxLayout(self.top_panel)
        top_layout.setContentsMargins(24, 16, 24, 16)
        top_layout.setSpacing(10)

        center_layout = QVBoxLayout(self.center_panel)
        center_layout.setContentsMargins(24, 16, 24, 16)

        bottom_layout = QVBoxLayout(self.bottom_panel)
        bottom_layout.setContentsMargins(24, 10, 24, 10)

        self.open_button = QPushButton("Open device")
        self.open_button.setStyleSheet(get_button_style())
        self.open_button.setEnabled(False)

        self.rescan_button = QPushButton("Rescan")
        self.rescan_button.setStyleSheet(get_button_style())

        top_layout.addWidget(self.rescan_button)
        top_layout.addWidget(self.open_button)

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
        self.selector.dropdown.currentIndexChanged.connect(self._on_device_selected)

    def _on_device_selected(self, index: int):
        if self.card is not None:
            self.open_button.setEnabled(False)
            self.status_label.setText("Close device panel before opening another device")
            return

        text = self.selector.dropdown.currentText()

        if index == 0:
            self.open_button.setEnabled(False)
            self.status_label.setText("Select a device and click Open device")
            return

        if "Unsupported" in text:
            self.open_button.setEnabled(False)
            self.status_label.setText("This device is not supported yet")
            return

        self.open_button.setEnabled(True)
        self.status_label.setText("Supported device selected")

    def _on_rescan_clicked(self):
        self.driver = None
        self.state = None

        try:
            supported, unsupported = find_tascam_devices()
        except Exception as e:
            supported = []
            unsupported = []
            self.status_label.setText(f"Real device scan failed, using mock: {e}")

        self.supported_devices = supported
        self.unsupported_devices = unsupported

        self.selector.dropdown.clear()
        self.selector.dropdown.addItem("Select device")

        for dev, desc in supported:
            self.selector.dropdown.addItem(desc.name)

        for dev, desc in unsupported:
            name = desc.name if desc else "Unknown device"
            self.selector.dropdown.addItem(f"{name} (Unsupported device)")

        if not supported and not unsupported:
            self.selector.dropdown.addItem("Mock Tascam US-4x4")

        self.selector.dropdown.setCurrentIndex(0)
        self.open_button.setEnabled(False)
        self.status_label.setText("Device list updated")

    def _on_open_clicked(self):
        if self.card is not None:
            self.status_label.setText("Device panel is already open")
            return

        try:
            fake = FakeTransport()
            fake.open()

            self.driver = US4X4Driver(fake)
            self.state = self.driver.read_device_state()

            self.card = US4x4Card(self.driver, self.state)
            self.card.closed.connect(self._on_card_closed)
            self.card.show()

            self.open_button.setEnabled(False)
            self.status_label.setText("Mock US-4x4 opened")

        except Exception as e:
            self.driver = None
            self.state = None
            self.card = None
            self.status_label.setText(f"Open failed: {e}")

    def _ensure_driver(self):
        if self.driver is None:
            self.status_label.setText("Device not opened")
            return False
        return True

    def _on_card_closed(self):
        self.card = None
        self.open_button.setEnabled(True)
        self.status_label.setText("Device panel closed")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())