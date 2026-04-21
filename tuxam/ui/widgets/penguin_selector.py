# ui/widgets/penguin_selector.py

from tuxam.ui.assets.assets_path import ASSETS_DIR
from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QStyledItemDelegate
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from tuxam.ui.styles import get_paper_dropdown_style


class PenguinSelector(QWidget):

    PENGUIN_SCROLL_PATH = ASSETS_DIR / "penguin_scroll.png"
    def __init__(self):
        super().__init__()
        self.setMinimumSize(400, 400)
        # --- penguin image ---
        self.penguin = QLabel(self)
        self.penguin.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.penguin.setStyleSheet("background: transparent;")
        self.penguin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pixmap = QPixmap(str(self.PENGUIN_SCROLL_PATH))
        self.penguin.setPixmap(self.pixmap)

        # --- dropdown ---
        self.dropdown = QComboBox(self)
        self.dropdown.setEditable(True)
        self.dropdown.lineEdit().setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dropdown.lineEdit().setReadOnly(True)
        self.dropdown.addItems([
            "Choose device...",
            "Tascam US-4x4",
            "Unsupported device",
        ])

        self.dropdown.setStyleSheet(get_paper_dropdown_style())
        self.dropdown.setItemDelegate(CenteredItemDelegate(self.dropdown))

    def resizeEvent(self, event):
        """Position elements dynamically"""

        w = self.width()
        h = self.height()

        # --- scale penguin ---

        scaled = self.pixmap.scaled(
            w,
            h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.penguin.setPixmap(scaled)

        # center penguin
        pw = scaled.width()
        ph = scaled.height()
        self.penguin.setGeometry(0, 0, w, h)

        # --- dropdown placement ---
        # IMPORTANT: you tweak these numbers once manually
        drop_width = int(pw * 0.6)
        drop_height = 40

        drop_x = (w - drop_width) // 2 + int(pw * 0.01)
        drop_y = int((h - ph) // 2 + ph * 0.45)

        self.dropdown.setGeometry(
            drop_x,
            drop_y,
            drop_width,
            drop_height
        )

class CenteredItemDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index, /):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignmentFlag.AlignCenter