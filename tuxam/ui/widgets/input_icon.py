# tuxam/ui/widgets/input_icon.py

from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QPushButton


class InputIcon(QPushButton):
    input_clicked = Signal(int)

    def __init__(self, index, off_image, on_image, button_size=90, icon_size=80):
        super().__init__()

        self.index = index
        self.enabled_state = False

        self.off_pixmap = QPixmap(str(off_image))
        self.on_pixmap = QPixmap(str(on_image))

        self.setFixedSize(button_size, button_size)
        self.setIconSize(QSize(icon_size, icon_size))
        self.setFlat(True)

        self.clicked.connect(self._emit_index)

        self.set_state(False)

    def _emit_index(self):
        self.input_clicked.emit(self.index)

    def set_state(self, enabled: bool):
        self.enabled_state = enabled
        pixmap = self.on_pixmap if enabled else self.off_pixmap
        self.setIcon(QIcon(pixmap))
