from __future__ import annotations

from PySide6.QtWidgets import QStackedWidget, QVBoxLayout, QWidget, QSizePolicy

from .equal_width_tabbar import EqualWidthTabBar


class TabsPanel(QWidget):
    """QTabBar + QStackedWidget (instead of QTabWidget)."""

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.tabbar = EqualWidthTabBar(self)
        self.tabbar.setExpanding(False)  # we do equal-width via tabSizeHint
        self.tabbar.setUsesScrollButtons(False)
        self.tabbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.stack = QStackedWidget(self)
        self.tabbar.currentChanged.connect(self.stack.setCurrentIndex)

        layout.addWidget(self.tabbar)
        layout.addWidget(self.stack, 1)

    def add_tab(self, page: QWidget, title: str) -> None:
        self.stack.addWidget(page)
        self.tabbar.addTab(title)

    def min_width_for_titles(self) -> int:
        return max(1, self.tabbar.count()) * self.tabbar.min_tab_width()
