from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget


class BaseTab(QWidget):
    """Shared UI for tabs."""

    def _init_page(self, title: str) -> QVBoxLayout:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        heading = QLabel(title)
        heading.setProperty("role", "heading")
        layout.addWidget(heading)

        return layout

    def _create_card(self) -> tuple[QFrame, QGridLayout]:
        card = QFrame()
        card.setProperty("role", "card")

        card_layout = QGridLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setHorizontalSpacing(12)
        card_layout.setVerticalSpacing(10)

        return card, card_layout
