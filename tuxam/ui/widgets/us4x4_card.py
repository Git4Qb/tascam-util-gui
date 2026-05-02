# tuxam/ui/widgets/us4x4_card.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal
from tuxam.devices.us_4x4.parameters import INPUT_CHANNEL
from tuxam.ui.widgets.input_icon import InputIcon
from tuxam.ui.assets.assets_path import ASSETS_DIR
from tuxam.ui.assets.icons.app_icon import get_app_icon


class US4x4Card(QWidget):
    closed = Signal()

    def __init__(self, driver, state):
        super().__init__()

        self.setWindowTitle("Tascam US-4x4 Settings Panel")
        self.setWindowIcon(get_app_icon())

        self.driver = driver
        self.state = state
        self.input_icons = []

        main_layout = QVBoxLayout(self)

        inputs_layout = QHBoxLayout()
        main_layout.addLayout(inputs_layout)

        off_image = ASSETS_DIR / "input_off.png"
        on_image = ASSETS_DIR / "input_on.png"

        for index in INPUT_CHANNEL:
            button = InputIcon(
                index,
                off_image,
                on_image,
                button_size=90,
                icon_size=80,
            )
            button.input_clicked.connect(self._on_input_clicked)

            inputs_layout.addWidget(button)
            self.input_icons.append(button)

    def _on_input_clicked(self, index: int):
        button = self.input_icons[index]
        new_state = not button.enabled_state

        button.set_state(new_state)

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)