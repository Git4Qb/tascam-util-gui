from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QWidget


class StatusBarWidget(QFrame):
    """Full-width status bar. Dumb UI; emits button clicks upward."""

    reconnect_clicked = Signal()
    save_profile_clicked = Signal()
    load_profile_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.setProperty("role", "statusBar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(10)

        self.status_label = QLabel("Status", self)

        self.save_profile_btn = QPushButton("Save profile", self)
        self.load_profile_btn = QPushButton("Load profile", self)
        self.reconnect_btn = QPushButton("Reconnect", self)

        self.save_profile_btn.clicked.connect(self.save_profile_clicked.emit)
        self.load_profile_btn.clicked.connect(self.load_profile_clicked.emit)
        self.reconnect_btn.clicked.connect(self.reconnect_clicked.emit)

        layout.addWidget(self.status_label, 1)
        layout.addWidget(self.save_profile_btn, 0)
        layout.addWidget(self.load_profile_btn, 0)
        layout.addWidget(self.reconnect_btn, 0)

    def set_status(self, text: str) -> None:
        self.status_label.setText(text)

    def set_reconnect_enabled(self, enabled: bool) -> None:
        self.reconnect_btn.setEnabled(enabled)

    def set_profiles_enabled(self, enabled: bool) -> None:
        self.save_profile_btn.setEnabled(enabled)
        self.load_profile_btn.setEnabled(enabled)