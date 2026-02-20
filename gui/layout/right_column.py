from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class RightColumnWidget(QWidget):
    """Dumb UI: planned/current text + action buttons. Emits clicks upward."""

    plan_clicked = Signal()
    confirm_clicked = Signal()
    cancel_clicked = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        planned_label = QLabel("Planned changes", self)
        self.planned_text = QTextEdit(self)
        self.planned_text.setReadOnly(True)

        current_label = QLabel("Current device state", self)
        self.current_state_text = QTextEdit(self)
        self.current_state_text.setReadOnly(True)
        self.current_state_text.setPlainText("Not loaded yet.")

        buttons_row = QWidget(self)
        buttons_layout = QHBoxLayout(buttons_row)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)

        self.plan_btn = QPushButton("Plan to apply", buttons_row)
        self.confirm_btn = QPushButton("Confirm changes", buttons_row)
        self.cancel_btn = QPushButton("Cancel", buttons_row)

        self.plan_btn.clicked.connect(self.plan_clicked.emit)
        self.confirm_btn.clicked.connect(self.confirm_clicked.emit)
        self.cancel_btn.clicked.connect(self.cancel_clicked.emit)

        buttons_layout.addWidget(self.plan_btn)
        buttons_layout.addWidget(self.confirm_btn)
        buttons_layout.addWidget(self.cancel_btn)

        layout.addWidget(planned_label, 0)
        layout.addWidget(self.planned_text, 1)
        layout.addWidget(current_label, 0)
        layout.addWidget(self.current_state_text, 1)
        layout.addWidget(buttons_row, 0)

    def set_planned_text(self, text: str) -> None:
        self.planned_text.setPlainText(text)

    def set_current_state_text(self, text: str) -> None:
        self.current_state_text.setPlainText(text)

    def set_buttons(self, *, plan: bool, confirm: bool, cancel: bool) -> None:
        self.plan_btn.setEnabled(plan)
        self.confirm_btn.setEnabled(confirm)
        self.cancel_btn.setEnabled(cancel)