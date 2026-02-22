# gui/tabs/inputs_tab.py

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
QCheckBox,
QFrame,
QHBoxLayout,
QLabel,
QVBoxLayout,
QWidget,
)

from core.device_state import DeviceState
from core.device_parameters import InputChannel


class InputsTab(QWidget):
    """
    UI-only tab: 4 input toggles (IN1..IN4).
    Emits input_changed(channel: InputChannel, enabled: bool).
    """
    input_changed = Signal(object, bool)

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
        hint.setProperty("role", "muted")
        card_layout.addWidget(hint)

        row = QWidget(card)
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(18)

        self._checks: dict[InputChannel, QCheckBox] = {}

        for ch, label in [
            (InputChannel.IN1, "Input 1"),
            (InputChannel.IN2, "Input 2"),
            (InputChannel.IN3, "Input 3"),
            (InputChannel.IN4, "Input 4"),
        ]:
            cb = QCheckBox(label, row)
            cb.setChecked(False)
            cb.toggled.connect(lambda checked, c=ch: self.input_changed.emit(c, bool(checked)))
            row_layout.addWidget(cb)
            self._checks[ch] = cb

        row_layout.addStretch(1)
        card_layout.addWidget(row)

        layout.addWidget(card)
        layout.addStretch(1)

    def set_from_device_state(self, s: DeviceState) -> None:
        # s.input_enable is [IN1..IN4] boolean-ish
        values = {
            InputChannel.IN1: bool(s.input_enable[0]) if len(s.input_enable) > 0 else False,
            InputChannel.IN2: bool(s.input_enable[1]) if len(s.input_enable) > 1 else False,
            InputChannel.IN3: bool(s.input_enable[2]) if len(s.input_enable) > 2 else False,
            InputChannel.IN4: bool(s.input_enable[3]) if len(s.input_enable) > 3 else False,
        }

        for ch, enabled in values.items():
            cb = self._checks.get(ch)
            if cb is None:
                continue
            cb.blockSignals(True)
            cb.setChecked(bool(enabled))
            cb.blockSignals(False)