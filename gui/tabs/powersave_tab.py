from PySide6.QtWidgets import QLabel, QPushButton, QComboBox

from gui.tabs.base_tab import BaseTab


class PowerSaveTab(BaseTab):
    """PowerSave tab UI."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = self._init_page("PowerSave")
        card, card_layout = self._create_card()

        self.mode_cb = QComboBox()
        self.mode_cb.addItems(["ON", "OFF"])

        card_layout.addWidget(QLabel("Mode:"), 0, 0)
        card_layout.addWidget(self.mode_cb, 0, 1)

        apply_btn = QPushButton("Apply powersave (placeholder)")
        apply_btn.setEnabled(False)
        card_layout.addWidget(apply_btn, 1, 0, 1, 2)

        layout.addWidget(card)
        layout.addStretch()

    def get_mode(self) -> str:
        return str(self.mode_cb.currentText()).upper()

    def set_mode(self, mode: str, *, emit: bool = False) -> None:
        if not emit:
            self.mode_cb.blockSignals(True)
        try:
            mode_u = str(mode).upper()
            idx = 0 if mode_u == "ON" else 1
            self.mode_cb.setCurrentIndex(idx)
        finally:
            if not emit:
                self.mode_cb.blockSignals(False)

    def set_from_device_state(self, s) -> None:
        """Apply powersave from DeviceState without emitting signals."""
        # DeviceState.powersave: bool
        self.set_mode("ON" if bool(getattr(s, "powersave", False)) else "OFF", emit=False)