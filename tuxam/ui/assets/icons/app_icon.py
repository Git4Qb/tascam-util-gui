# tuxam/ui/assets/app_icon.py

from PySide6.QtGui import QIcon
from tuxam.ui.assets.assets_path import icon

def get_app_icon() -> QIcon:
    app_icon = QIcon()

    for size in [16, 32, 48, 128, 256]:
        app_icon.addFile(icon(f'tuxam_icon_{size}.png'))

    return app_icon

