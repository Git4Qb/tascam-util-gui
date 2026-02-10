from PySide6.QtWidgets import QLabel, QPushButton, QComboBox

from gui.tabs.base_tab import BaseTab


class MonitoringTab(BaseTab):
    """Monitoring tab UI."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = self._init_page("Monitoring")
        card, card_layout = self._create_card()

        input_cb = QComboBox()
        input_cb.addItems(["IN12", "IN34"])

        mode_cb = QComboBox()
        mode_cb.addItems(["MONO", "STEREO"])

        card_layout.addWidget(QLabel("Input pair:"), 0, 0)
        card_layout.addWidget(input_cb, 0, 1)

        card_layout.addWidget(QLabel("Mode:"), 1, 0)
        card_layout.addWidget(mode_cb, 1, 1)

        apply_btn = QPushButton("Apply monitoring (placeholder)")
        apply_btn.setEnabled(False)
        card_layout.addWidget(apply_btn, 2, 0, 1, 2)

        layout.addWidget(card)
        layout.addStretch()
