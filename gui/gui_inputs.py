import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel, QComboBox, QHBoxLayout, QMessageBox, QCheckBox
import subprocess
# TODO "device not found / device connected" info
# TODO input active checkboxes
# TODO routing outputs how to
class TascamControlGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 300, 400)

        # Main layout
        self.
        main_layout = QVBoxLayout()

        for item in inputs:
            self.checkbox = QCheckBox(inputs[item])



#
#         # Direct Monitor Section
#         monitor_label = QLabel("Monitor Settings")
#         self.monitor_input = QComboBox()
#         self.monitor_input.addItems(["IN 1 2", "IN 3 4"])
#
#         self.monitor_mode = QComboBox()
#         self.monitor_mode.addItems(["MONO", "STEREO"])
#
#         monitor_button = QPushButton("Set Monitor")
#         monitor_button.clicked.connect(self.set_monitor)
#
#         # Layout for monitor section
#         monitor_layout = QHBoxLayout()
#         monitor_layout.addWidget(self.monitor_input)
#         monitor_layout.addWidget(self.monitor_mode)
#         monitor_layout.addWidget(monitor_button)
#
#
#
#
#
#
#
#
#
#
#         # Audio Input Section
#         input_label = QLabel("Enable Inputs")
#         self.input_in1 = QCheckBox("IN 1", self)
#         self.input_in2 = QCheckBox("IN 2", self)
#         self.input_in3 = QCheckBox("IN 3", self)
#         self.input_in4 = QCheckBox("IN 4", self)
#
#         self.input_mode = QComboBox()
#         self.input_mode.addItems(["ON", "OFF"])
#
#         input_button = QPushButton("Set Input")
#         input_button.clicked.connect(self.set_input)
#
#         # Layout for input section
#         input_layout = QHBoxLayout()
#         input_layout.addWidget(self.input_in1)
#         input_layout.addWidget(self.input_in2)
#         input_layout.addWidget(self.input_in3)
#         input_layout.addWidget(self.input_in4)
#
#         # Connect each checkbox's state change to the apply_settings method
#         self.input_in1.stateChanged.connect(lambda: self.set_input("IN 1", self.input_in1.isChecked()))
#         self.input_in2.stateChanged.connect(lambda: self.set_input("IN 2", self.input_in2.isChecked()))
#         self.input_in3.stateChanged.connect(lambda: self.set_input("IN 3", self.input_in3.isChecked()))
#         self.input_in4.stateChanged.connect(lambda: self.set_input("IN 4", self.input_in4.isChecked()))
#
#
#         # Power Saving Section
#         powersave_label = QLabel("Power Save Settings")
#         self.powersave_mode = QComboBox()
#         self.powersave_mode.addItems(["ON", "OFF"])
#
#         powersave_button = QPushButton("Set Power Save")
#         powersave_button.clicked.connect(self.set_powersave)
#
#         # Layout for powersave section
#         powersave_layout = QHBoxLayout()
#         powersave_layout.addWidget(self.powersave_mode)
#         powersave_layout.addWidget(powersave_button)
#
#         # Adding sections to main layout
#         main_layout.addWidget(route_label)
#         main_layout.addLayout(route_layout)
#
#         main_layout.addWidget(monitor_label)
#         main_layout.addLayout(monitor_layout)
#
#         main_layout.addWidget(input_label)
#         main_layout.addLayout(input_layout)
#
#         main_layout.addWidget(powersave_label)
#         main_layout.addLayout(powersave_layout)
#
#         # Set central widget and layout
#         container = QWidget()
#         container.setLayout(main_layout)
#         self.setCentralWidget(container)
#
#     def run_command(self, command):
#         """Utility function to run command-line commands"""
#         try:
#             subprocess.run(command, check=True, shell=True)
#             QMessageBox.information(self, "Success", "Command executed successfully.")
#         except subprocess.CalledProcessError as e:
#             QMessageBox.critical(self, "Error", f"Error executing command: {str(e)}")
#
#     def set_route(self):
#         """Set route command"""
#         source = self.route_source.currentText()
#         dest = self.route_dest.currentText()
#         command = f"python tascam-util.py route -s {source} -d {dest}"
#         self.run_command(command)
#
#     def set_monitor(self):
#         """Set monitor command"""
#         input_pair = self.monitor_input.currentText()
#         mode = self.monitor_mode.currentText()
#         command = f"python tascam-util.py monitor -i {input_pair} -m {mode}"
#         subprocess.run(command, shell=True)  # Execute the command
#         self.run_command(command)
#
#     def set_input(self, input_name, enabled):
#         """Set input command"""
#         mode = "ON" if enabled else "OFF"
#         command = f"python tascam-util.py input -i {input_name} -m {mode}"
#         self.run_command(command)
#
#     def set_powersave(self):
#         """Set power saving command"""
#         mode = self.powersave_mode.currentText()
#         command = f"python tascam-util.py powersave -m {mode}"
#         self.run_command(command)
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#
#     window = TascamControlGUI()
#     window.show()
#
#     sys.exit(app.exec())
