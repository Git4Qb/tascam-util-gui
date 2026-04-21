# tools/test_png.py

import sys
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from tuxam.ui.assets.assets_path import ASSETS_DIR

app = QApplication(sys.argv)

label = QLabel()
label.setAlignment(Qt.AlignmentFlag.AlignCenter)

pixmap = QPixmap(str(ASSETS_DIR / "fixed_penguin.png"))

print("Loaded:", not pixmap.isNull())

label.setPixmap(pixmap)
label.resize(600, 600)
label.show()

sys.exit(app.exec())
