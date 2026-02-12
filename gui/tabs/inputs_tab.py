# gui/tabs/inputs_tab.py

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget


class InputsTab(QWidget):
    """
    UI-only tab: 4 input toggles (IN1..IN4).
    Emits input_changed(input_name, mode) where mode is "ON" / "OFF".
    """
    input_changed = Signal(str, str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        heading = QLabel("Inputs", self)
        heading.setProperty("role", "heading")
        layout.addWidget(heading)

        card = QFrame(self)
        card.setProperty("role", "card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(10)

        hint = QLabel("Enable/disable device inputs (checked = ON).", card)
        card_layout.addWidget(hint)

        row = QWidget(card)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(18)

        self._checks: dict[str, QCheckBox] = {}

        for name in ("IN1", "IN2", "IN3", "IN4"):
            cb = QCheckBox(name, row)
            cb.setChecked(False)
            cb.toggled.connect(lambda checked, n=name: self._emit_change(n, checked))
            row_layout.addWidget(cb)
            self._checks[name] = cb

        row_layout.addStretch(1)
        card_layout.addWidget(row)

        layout.addWidget(card)
        layout.addStretch(1)

    def _emit_change(self, input_name: str, checked: bool) -> None:
        mode = "ON" if checked else "OFF"
        self.input_changed.emit(input_name, mode)
