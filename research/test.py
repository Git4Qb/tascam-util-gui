import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QCheckBox, QLabel


class CheckBoxExample(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the layout
        layout = QVBoxLayout()

        # Create a checkbox
        self.checkbox = QCheckBox("I agree to the terms and conditions")
        self.checkbox.stateChanged.connect(self.check_checkbox_state)  # Connect state change signal
        layout.addWidget(self.checkbox)

        # Create a label to display the result
        self.result_label = QLabel("Checkbox not checked")
        layout.addWidget(self.result_label)

        # Set the layout for the main window
        self.setLayout(layout)

    def check_checkbox_state(self):
        # Automatically check the state of the checkbox
        if self.checkbox.isChecked():
            self.result_label.setText("Checkbox is checked")
        else:
            self.result_label.setText("Checkbox is not checked")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window
    window = CheckBoxExample()
    window.setWindowTitle("Checkbox Example")
    window.show()

    sys.exit(app.exec())
