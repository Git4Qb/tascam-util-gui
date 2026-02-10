import sys
from pathlib import Path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """Main application window containing placeholder tabs."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("TASCAM Utility")
        self.resize(900, 600)

        tabs = QTabWidget(self)
        self.setCentralWidget(tabs)

        # Routing tab: now uses a simple panel/card layout
        tabs.addTab(self._create_routing_tab(), "Routing")

        # Other tabs unchanged (placeholders)
        tabs.addTab(self._create_monitoring_tab(), "Monitoring")
        tabs.addTab(self._create_placeholder_tab("Inputs"), "Inputs")
        tabs.addTab(self._create_placeholder_tab("PowerSave"), "PowerSave")

    def _create_routing_tab(self) -> QWidget:
        """Create a simple card-like layout for the Routing tab."""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(16, 16, 16, 16)
        page_layout.setSpacing(12)

        # Optional heading
        heading = QLabel("Routing")
        heading.setProperty("role", "heading")
        page_layout.addWidget(heading)

        # Card / panel
        card = QFrame()
        card.setProperty("role", "card")
        card.setFrameShape(QFrame.StyledPanel)


        card_layout = QGridLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setHorizontalSpacing(12)
        card_layout.setVerticalSpacing(10)

        # Placeholder content inside the card
        card_layout.addWidget(QLabel("Source:"), 0, 0)
        card_layout.addWidget(QLabel("—"), 0, 1)

        card_layout.addWidget(QLabel("Destination:"), 1, 0)
        card_layout.addWidget(QLabel("—"), 1, 1)

        apply_btn = QPushButton("Apply (placeholder)")
        apply_btn.setEnabled(False)
        card_layout.addWidget(apply_btn, 2, 0, 1, 2)

        page_layout.addWidget(card)
        page_layout.addStretch()

        return page

    def _create_monitoring_tab(self) -> QWidget:
        """Create a simple card-like layout for the Monitoring tab."""
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(16, 16, 16, 16)
        page_layout.setSpacing(12)

        heading = QLabel("Monitoring")
        heading.setProperty("role", "heading")
        page_layout.addWidget(heading)

        card = QFrame()
        card.setProperty("role", "card")
        card.setFrameShape(QFrame.StyledPanel)

        card_layout = QGridLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setHorizontalSpacing(12)
        card_layout.setVerticalSpacing(10)

        card_layout.addWidget(QLabel("Monitor source:"), 0, 0)
        card_layout.addWidget(QLabel("—"), 0, 1)

        card_layout.addWidget(QLabel("Level:"), 1, 0)
        card_layout.addWidget(QLabel("—"), 1, 1)

        refresh_btn = QPushButton("Refresh (placeholder)")
        refresh_btn.setEnabled(False)
        card_layout.addWidget(refresh_btn, 2, 0, 1, 2)

        page_layout.addWidget(card)
        page_layout.addStretch()

        return page

    @staticmethod
    def _create_placeholder_tab(name: str) -> QWidget:
        """Create a tab page with a centered placeholder label."""
        page = QWidget()
        layout = QVBoxLayout(page)

        label = QLabel(f"{name} tab placeholder")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(label)
        return page


def main() -> int:
    """Run the tab skeleton window."""
    app = QApplication(sys.argv)
    qss = Path(__file__).parent / "style.qss"
    app.setStyleSheet(qss.read_text(encoding="utf-8"))
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
