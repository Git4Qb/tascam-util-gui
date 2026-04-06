# tuxam/ui/main_window.py

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import  QColor
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
    get_background_frame_style,
    get_panel_style,
)

from tuxam.ui.widgets.penguin_selector import PenguinSelector


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tuxam")
        self.resize(560, 640)

        self.setStyleSheet(get_main_window_style())

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(20, 20, 20, 20)

        self.bg_frame = QFrame()
        self.bg_frame.setStyleSheet(get_background_frame_style())

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
        self.open_button.setEnabled(True)

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

    def _on_device_selected(self, index: int):
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
        # placeholder for real USB rescan logic
        self.status_label.setText("Device list rescanned")

    def _on_open_clicked(self):
        selected = self.selector.ldown.currentText()
        self.status_label.setText(f"Opening window for: {selected}")
        print(f"Open device window for: {selected}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())