import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QRadioButton, QButtonGroup, QLabel

class RadioButtonExample(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Radio Button Example")
        self.setGeometry(100, 100, 300, 200)

        # Create layout
        layout = QVBoxLayout()

        # Create a QLabel to display the selected option
        self.label = QLabel("Selected option: ", self)
        layout.addWidget(self.label)

        # Create radio buttons
        self.radio_option1 = QRadioButton("Option 1", self)
        self.radio_option2 = QRadioButton("Option 2", self)
        self.radio_option3 = QRadioButton("Option 3", self)

        # Set default selected radio button (e.g., "Option 2")
        self.radio_option1.setChecked(True)

        # Add radio buttons to the layout
        layout.addWidget(self.radio_option1)
        layout.addWidget(self.radio_option2)
        layout.addWidget(self.radio_option3)

        # Create a button group to group the radio buttons
        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.radio_option1)
        self.button_group.addButton(self.radio_option2)
        self.button_group.addButton(self.radio_option3)

        # Connect the button group's signal to a method to handle selection
        self.button_group.buttonClicked.connect(self.radio_selection_changed)

        # Set the layout for the window
        self.setLayout(layout)

        # Update the label to reflect the default selection
        self.label.setText(f"Selected option: {self.button_group.checkedButton().text()}")

    # Method to handle radio button selection changes
    def radio_selection_changed(self, button):
        self.label.setText(f"Selected option: {button.text()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RadioButtonExample()
    window.show()
    sys.exit(app.exec())
