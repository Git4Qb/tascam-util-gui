from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QCheckBox,
)

from gui.tabs import RoutingTab, MonitoringTab, InputsTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TASCAMUS 4x4")
        self.resize(680, 720)

        root = QWidget()
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # LEFT COLUMN ---------------------------------------------------------
        left_col = QWidget()
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        self.tabs = QTabWidget()
        self.tabs.addTab(RoutingTab(), "Routing")
        self.tabs.addTab(MonitoringTab(), "Monitoring")
        self.tabs.addTab(InputsTab(), "Inputs")

        # PowerSave panel
        self.powersave_panel = QFrame()
        ps_layout = QVBoxLayout(self.powersave_panel)
        ps_layout.setContentsMargins(8, 8, 8, 8)
        ps_layout.setSpacing(6)

        ps_layout.addWidget(QLabel("PowerSave"))

        self.powersave_toggle = QCheckBox("Enabled")
        self.powersave_toggle.setChecked(False)
        ps_layout.addWidget(self.powersave_toggle)

        left_layout.addWidget(self.tabs, 1)
        left_layout.addWidget(self.powersave_panel, 0)

        # RIGHT COLUMN --------------------------------------------------------
        right_col = QWidget()
        right_layout = QVBoxLayout(right_col)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # Planned/future state
        planned_label = QLabel("Planned changes")
        self.planned_text = QTextEdit()
        self.planned_text.setReadOnly(True)
        self.planned_text.setPlainText("Changes you want to make:")

        # Current real device state
        current_label = QLabel("Current device state")
        self.current_state_text = QTextEdit()
        self.current_state_text.setReadOnly(True)
        self.current_state_text.setPlainText("Not loaded yet.")

        # Buttons
        buttons_row = QWidget()
        buttons_layout = QHBoxLayout(buttons_row)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)

        self.plan_btn = QPushButton("Plan to apply")
        self.confirm_btn = QPushButton("Confirm changes")
        self.cancel_btn = QPushButton("Cancel")

        # initial state
        self.confirm_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)

        buttons_layout.addWidget(self.plan_btn)
        buttons_layout.addWidget(self.confirm_btn)
        buttons_layout.addWidget(self.cancel_btn)

        right_layout.addWidget(planned_label, 0)
        right_layout.addWidget(self.planned_text, 1)
        right_layout.addWidget(current_label, 0)
        right_layout.addWidget(self.current_state_text, 1)
        right_layout.addWidget(buttons_row, 0)

        main_layout.addWidget(left_col, 3)
        main_layout.addWidget(right_col, 2)
