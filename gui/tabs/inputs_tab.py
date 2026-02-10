from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
    QPushButton,
)


class RoutingTab(QWidget):
    """Inputs tab UI."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Heading
        heading = QLabel("Inputs")
        heading.setProperty("role", "heading")
        layout.addWidget(heading)

        # Card / panel
        card = QFrame()
        card.setProperty("role", "card")

        card_layout = QGridLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setHorizontalSpacing(12)
        card_layout.setVerticalSpacing(10)

        card_layout.addWidget(QLabel("Source:"), 0, 0)
        card_layout.addWidget(QLabel("—"), 0, 1)

        card_layout.addWidget(QLabel("Destination:"), 1, 0)
        card_layout.addWidget(QLabel("—"), 1, 1)

        apply_btn = QPushButton("Apply (placeholder)")
        apply_btn.setEnabled(False)
        card_layout.addWidget(apply_btn, 2, 0, 1, 2)

        layout.addWidget(card)
        layout.addStretch()
