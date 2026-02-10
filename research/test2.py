import usb.core
import usb.util
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

# Define vendor and product IDs
VENDOR_ID = 0x0644  # Replace with actual vendor ID
PRODUCT_ID = 0x804e  # Replace with actual product ID

# Find the USB device
device = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if device is None:
    raise ValueError('Device not found')

# Set the active configuration. With no arguments, the first configuration will be the active one.
device.set_configuration()

def send_command(bmRequestType, bRequest, wValue, wIndex, wLength, data=None):
    """Send a control transfer command to the USB device."""
    try:
        device.ctrl_transfer(bmRequestType, bRequest, wValue, wIndex, data or bytearray(wLength))
        QMessageBox.information(None, "Success", "Command sent successfully!")
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to send command: {e}")

def on_send_button_click():
    """Handle the button click event."""
    bmRequestType = 0x40  # Host-to-device, Vendor
    bRequest = 6          # Replace with your specific request
    wValue = 0x0001      # Replace with your specific value
    wIndex = 0           # Replace with your specific index
    wLength = 0          # Data length

    send_command(bmRequestType, bRequest, wValue, wIndex, wLength)

# Create the GUI application
app = QApplication([])

# Create the main window
window = QWidget()
window.setWindowTitle("Tascam US-4x4 Control")

# Create a button to send commands
send_button = QPushButton("Send Command")
send_button.clicked.connect(on_send_button_click)

# Set up the layout
layout = QVBoxLayout()
layout.addWidget(send_button)
window.setLayout(layout)

# Show the window
window.show()

# Run the application
app.exec()
