import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QLabel

class IORoute(QWidget):
    def __init__(self):
        super().__init__()

        # Route Section
        route_label = QLabel("Route Settings")

        route_options = ["Input/Computer MIX", "Computer OUT 1/2", "Computer OUT 3/4"]

        # Static label for LINE12
        line12_label = QLabel("LINE OUT 1/2")
        self.line12_source = QComboBox()
        self.line12_source.addItems(route_options)

        # Static label for LINE34
        line12_label = QLabel("LINE OUT 3/4")
        self.line34_source = QComboBox()
        self.line34_source.addItems(route_options)



        # Layout for route section
        route_layout = QVBoxLayout()
        route_layout.addWidget(self.route_source)
        route_layout.addWidget(self.route_dest)
        # Create layout
        layout = QVBoxLayout()




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
