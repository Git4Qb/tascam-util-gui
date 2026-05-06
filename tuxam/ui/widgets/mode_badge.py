# tuxam/ui/widgets/mode_badge.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class ModeBadge(QLabel):
    def __init__(self, text: str):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #e83706;
                color: black;
                font-weight: bold;
                border-radius: 8px;
                padding: 4px 10px;
            }
        """)