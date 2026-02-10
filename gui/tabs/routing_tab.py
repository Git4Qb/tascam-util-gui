from PySide6.QtWidgets import QLabel, QPushButton, QComboBox

from gui.tabs.base_tab import BaseTab


class RoutingTab(BaseTab):
    """Routing tab UI."""

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = self._init_page("Routing")
        card, card_layout = self._create_card()

        source_cb = QComboBox()
        source_cb.addItems(["MIX", "OUT12", "OUT34"])

        dest_cb = QComboBox()
        dest_cb.addItems(["LINE12", "LINE34"])

        card_layout.addWidget(QLabel("Source:"), 0, 0)
        card_layout.addWidget(source_cb, 0, 1)

        card_layout.addWidget(QLabel("Destination:"), 1, 0)
        card_layout.addWidget(dest_cb, 1, 1)

        apply_btn = QPushButton("Apply routing (placeholder)")
        apply_btn.setEnabled(False)
        card_layout.addWidget(apply_btn, 2, 0, 1, 2)

        layout.addWidget(card)
        layout.addStretch()
