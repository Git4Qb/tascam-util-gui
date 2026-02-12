import sys
from sys import modules

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
import usb.core
import usb.util

# Import functions from tascam-util
from cli_core.powersave import set_powersave_mode, get_mode_id

class TascamController(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tascam US-4x4 Controller")
        self.setGeometry(300, 300, 300, 200)

        self.layout = QVBoxLayout()

        self.label = QLabel("Select Power Save Mode:")
        self.layout.addWidget(self.label)

        self.power_on_button = QPushButton("Power Save Mode ON")
        self.power_off_button = QPushButton("Power Save Mode OFF")

        self.power_on_button.clicked.connect(self.set_power_mode_on)
        self.power_off_button.clicked.connect(self.set_power_mode_off)

        self.layout.addWidget(self.power_on_button)
        self.layout.addWidget(self.power_off_button)

        self.setLayout(self.layout)

        # Initialize Tascam device
        self.device = self.find_tascam_device()

    def find_tascam_device(self):
        # Replace with your device's Vendor ID and Product ID
        VID = 0x0644  # Example Vendor ID
        PID = 0x804e  # Example Product ID

        device = usb.core.find(idVendor=VID, idProduct=PID)
        if device is None:
            QMessageBox.critical(self, "Error", "Tascam US-4x4 device not found.")
            sys.exit()

        usb.util.claim_interface(device, 0)  # Claim the first interface
        return device

    def set_power_mode_on(self):
        try:
            set_powersave_mode(self.device, get_mode_id("ON"))
            QMessageBox.information(self, "Success", "Power save mode enabled.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def set_power_mode_off(self):
        try:
            set_powersave_mode(self.device, get_mode_id("OFF"))
            QMessageBox.information(self, "Success", "Power save mode disabled.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = TascamController()
    controller.show()
    sys.exit(app.exec())
