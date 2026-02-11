from __future__ import annotations

from PySide6.QtCore import QSize, QEvent
from PySide6.QtWidgets import QTabBar, QStyle, QStyleOptionTab


class EqualWidthTabBar(QTabBar):
    """
    TabBar with equal-width tabs that also fill 100% of available width.

    Sizing logic intentionally matches the proven working approach:
        w = max(min_each, self.width() // n)
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cached_min_each: int | None = None

    # ---- cache helpers ----
    def _invalidate_min_width_cache(self) -> None:
        self._cached_min_each = None
        # geometry update is enough; no need to force repaint manually
        self.updateGeometry()

    def tabInserted(self, index: int) -> None:
        super().tabInserted(index)
        self._invalidate_min_width_cache()

    def tabRemoved(self, index: int) -> None:
        super().tabRemoved(index)
        self._invalidate_min_width_cache()

    def changeEvent(self, event: QEvent) -> None:
        # font/style changes can alter metrics → recalc min tab width
        if event.type() in (QEvent.Type.FontChange, QEvent.Type.StyleChange):
            self._invalidate_min_width_cache()
        super().changeEvent(event)

    # ---- public helper ----
    def min_tab_width(self) -> int:
        return self._min_single_tab_width()

    # ---- sizing logic ----
    def _min_single_tab_width(self) -> int:
        # Cached because tabSizeHint() can be called many times during layout/paint
        if self._cached_min_each is not None:
            return self._cached_min_each

        worst = 0
        for i in range(max(1, self.count())):
            opt = QStyleOptionTab()
            self.initStyleOption(opt, i)

            text_w = opt.fontMetrics.horizontalAdvance(opt.text)

            # Style-aware sizing (includes QSS padding, etc.)
            w = self.style().sizeFromContents(
                QStyle.ContentsType.CT_TabBarTab,
                opt,
                QSize(text_w, 0),
                self,
            ).width()

            worst = max(worst, w)

        self._cached_min_each = worst
        return worst

    def tabSizeHint(self, index: int) -> QSize:
        size = super().tabSizeHint(index)

        n = max(1, self.count())
        min_each = self._min_single_tab_width()

        # IDENTICAL EFFECT: equal-width + fill 100%
        w = max(min_each, self.width() // n)
        size.setWidth(w)
        return size

    def resizeEvent(self, e) -> None:
        super().resizeEvent(e)
        self.updateGeometry()
