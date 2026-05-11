from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QWidget

from tuxam.ui.assets.assets_path import penguin
from tuxam.ui.styles import (
    get_button_style,
    get_empty_state_detail_style,
    get_empty_state_title_style,
    get_primary_button_style,
)


class NoDeviceView(QWidget):
    rescan_requested = Signal()
    demo_mode_requested = Signal()
    quit_requested = Signal()

    PENGUIN_NO_DEVICE_PATH = penguin("penguin_no_device.png")

    def __init__(self):
        super().__init__()
        self.setMinimumSize(560, 560)
        self._pixmap = QPixmap(str(self.PENGUIN_NO_DEVICE_PATH))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 22, 28, 24)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet(get_empty_state_title_style())

        self.detail_label = QLabel()
        self.detail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet(get_empty_state_detail_style())

        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rescan_button = QPushButton("Rescan")
        self.demo_button = QPushButton("Demo Mode")
        self.quit_button = QPushButton("Quit")

        self.rescan_button.setStyleSheet(get_primary_button_style())
        for button in (self.demo_button, self.quit_button):
            button.setStyleSheet(get_button_style())
            button_layout.addWidget(button)
        button_layout.insertWidget(0, self.rescan_button)

        layout.addStretch(1)
        layout.addWidget(self.image_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.detail_label)
        layout.addLayout(button_layout)
        layout.addStretch(1)

        self.rescan_button.clicked.connect(self.rescan_requested.emit)
        self.demo_button.clicked.connect(self.demo_mode_requested.emit)
        self.quit_button.clicked.connect(self.quit_requested.emit)

    def show_real_no_devices(self):
        self.rescan_button.setText("Rescan")
        self.title_label.setText("No Tascam device found")
        self.detail_label.setText(
            "Connect a Tascam USB interface and rescan, or open Demo Mode."
        )
        self.demo_button.setVisible(True)

    def show_no_demo_devices(self):
        self.rescan_button.setText("Rescan")
        self.title_label.setText("No demo devices available")
        self.detail_label.setText("This app version does not provide any simulated devices.")
        self.demo_button.setVisible(False)

    def show_scan_error(self, error):
        self.rescan_button.setText("Try Again")
        self.title_label.setText("Device scan failed")
        self.detail_label.setText(f"Could not scan USB devices: {error}")
        self.demo_button.setVisible(True)

    def resizeEvent(self, event):
        if not self._pixmap.isNull():
            max_width = max(220, int(self.width() * 0.58))
            max_height = max(220, int(self.height() * 0.52))
            scaled = self._pixmap.scaled(
                max_width,
                max_height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled)

        super().resizeEvent(event)
