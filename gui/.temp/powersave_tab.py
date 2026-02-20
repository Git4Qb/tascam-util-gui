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

        mode_cb = QComboBox()
        mode_cb.addItems(["ON", "OFF"])

        card_layout.addWidget(QLabel("Mode:"), 0, 0)
        card_layout.addWidget(mode_cb, 0, 1)

        apply_btn = QPushButton("Apply powersave (placeholder)")
        apply_btn.setEnabled(False)
        card_layout.addWidget(apply_btn, 1, 0, 1, 2)

        layout.addWidget(card)
        layout.addStretch()
