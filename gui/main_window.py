"""Main window skeleton with tabs only.

This module intentionally contains only GUI layout scaffolding.
No device/core logic should be imported here.
"""

from __future__ import annotations

import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QTabWidget, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    """Main application window containing placeholder tabs."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("TASCAM Utility")
        self.resize(900, 600)

        tabs = QTabWidget(self)
        self.setCentralWidget(tabs)

        tabs.addTab(self._create_placeholder_tab("Routing"), "Routing")
        tabs.addTab(self._create_placeholder_tab("Monitoring"), "Monitoring")
        tabs.addTab(self._create_placeholder_tab("Inputs"), "Inputs")
        tabs.addTab(self._create_placeholder_tab("PowerSave"), "PowerSave")

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
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
