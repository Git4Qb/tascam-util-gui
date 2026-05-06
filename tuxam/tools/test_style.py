# tuxam/tools/test_style.py

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QColor, QPen, QBrush
from PySide6.QtCore import Qt


class AnimatedHoverButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

        self._hover_progress = 0.0

        self._animation = QPropertyAnimation(self, b"hover_progress", self)
        self._animation.setDuration(180)
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(36)

        self.normal_bg = QColor("#d6d6d6")
        self.hover_bg = QColor("#333333")
        self.border_color = QColor("#5a5a5a")
        self.text_color = QColor("#2C2C2C")
        self.hover_text_color = QColor("#F5F5F5")

        self.radius = 8
        self.padding_x = 12

    def get_hover_progress(self):
        return self._hover_progress

    def set_hover_progress(self, value):
        self._hover_progress = value
        self.update()

    hover_progress = Property(float, get_hover_progress, set_hover_progress)

    def enterEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self._hover_progress)
        self._animation.setEndValue(1.0)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.stop()
        self._animation.setStartValue(self._hover_progress)
        self._animation.setEndValue(0.0)
        self._animation.start()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(1, 1, -1, -1)

        # normal background
        painter.setPen(QPen(self.border_color, 1))
        painter.setBrush(QBrush(self.normal_bg))
        painter.drawRoundedRect(rect, self.radius, self.radius)

        # animated hover overlay
        overlay_width = int(self.width() * self._hover_progress)
        if overlay_width > 0:
            overlay_rect = rect
            overlay_rect.setWidth(overlay_width)

            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(self.hover_bg))
            painter.drawRoundedRect(overlay_rect, self.radius, self.radius)

        # text
        if self._hover_progress > 0.5:
            painter.setPen(self.hover_text_color)
        else:
            painter.setPen(self.text_color)

        painter.drawText(
            rect,
            Qt.AlignmentFlag.AlignCenter,
            self.text()
        )