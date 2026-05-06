# ui/widgets/penguin_selector.py

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QListWidget,
    QListWidgetItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont

from tuxam.ui.assets.assets_path import penguin
from tuxam.ui.styles import get_device_list_style


class PenguinSelector(QWidget):
    PENGUIN_SCROLL_PATH = penguin("penguin_select_device.png")

    def __init__(self):
        super().__init__()
        self.setMinimumSize(560, 560)

        # --- penguin image ---
        self.penguin = QLabel(self)
        self.penguin.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.penguin.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.pixmap = QPixmap(str(self.PENGUIN_SCROLL_PATH))
        self.penguin.setPixmap(self.pixmap)

        # --- device list ---
        self.device_list = QListWidget(self)
        self.device_list.addItems([
            "Select device...",
            "Tascam US-4x4",
            "Unsupported device",
        ])

        self.device_list.setFrameShape(QListWidget.Shape.NoFrame)
        self.device_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.device_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.device_list.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.device_list.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.device_list.setAutoFillBackground(False)
        self.device_list.viewport().setAutoFillBackground(False)
        self.device_list_font = QFont()

        self.device_list.setStyleSheet(get_device_list_style())

    def set_title_item(self, text: str):
        title_item = QListWidgetItem(text)
        title_item.setFlags(Qt.ItemFlag.NoItemFlags)
        self.device_list.addItem(title_item)

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()

        # --- scale penguin ---
        scaled = self.pixmap.scaled(
            w,
            h,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.penguin.setPixmap(scaled)
        self.penguin.setGeometry(0, 0, w, h)

        pw = scaled.width()
        ph = scaled.height()

        image_x = (w - pw) // 2
        image_y = (h - ph) // 2

        # device list position
        list_x_on_image = 550
        list_y_on_image = 320
        list_w_on_image = 340
        list_h_on_image = 400

        scale = pw / self.pixmap.width()

        list_x = int(image_x + list_x_on_image * scale)
        list_y = int(image_y + list_y_on_image * scale)
        list_w = int(list_w_on_image * scale)
        list_h = int(list_h_on_image * scale)

        self.device_list.setGeometry(
            list_x,
            list_y,
            list_w,
            list_h,
        )

        self.device_list.raise_()

        base_widget_width = 560
        base_font_size = 14.0

        font_scale = pw / base_widget_width
        scaled_font_size = max(14.0, base_font_size * font_scale)

        self.device_list_font.setPointSizeF(scaled_font_size)
        self.device_list.setFont(self.device_list_font)
        self.device_list.setStyleSheet(get_device_list_style(int(scaled_font_size)))

        super().resizeEvent(event)