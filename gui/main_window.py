from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from gui.tabs import InputsTab, MonitoringTab, RoutingTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TASCAMUS 4x4")
        self.resize(900, 720)

        root = QWidget(self)
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # LEFT COLUMN ---------------------------------------------------------
        left_col = QWidget(self)
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        self.tabs = QTabWidget(left_col)
        tabbar = self.tabs.tabBar()
        tabbar.setExpanding(True)
        self.tabs.setUsesScrollButtons(False)
        self.tabs.setElideMode(Qt.TextElideMode.ElideNone)

        self.tabs.addTab(RoutingTab(), "Routing")
        self.tabs.addTab(MonitoringTab(), "Monitoring")
        self.tabs.addTab(InputsTab(), "Inputs")

        sep = QFrame(left_col)
        sep.setProperty("role", "sectionSeparator")
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)

        self.powersave_panel = QFrame(left_col)
        ps_layout = QHBoxLayout(self.powersave_panel)
        ps_layout.setContentsMargins(8, 6, 8, 6)
        ps_layout.setSpacing(8)

        ps_title = QLabel("PowerSave", self.powersave_panel)
        ps_title.setProperty("role", "heading")

        ps_enabled = QLabel("Enabled", self.powersave_panel)
        ps_enabled.setProperty("role", "heading")

        self.powersave_toggle = QCheckBox(self.powersave_panel)
        self.powersave_toggle.setChecked(False)

        ps_layout.addWidget(ps_title)
        ps_layout.addStretch(1)
        ps_layout.addWidget(ps_enabled)
        ps_layout.addWidget(self.powersave_toggle)

        left_layout.addWidget(self.tabs, 1)
        left_layout.addWidget(sep, 0)
        left_layout.addWidget(self.powersave_panel, 0)

        # RIGHT COLUMN --------------------------------------------------------
        right_col = QWidget(self)
        right_layout = QVBoxLayout(right_col)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        planned_label = QLabel("Planned changes", right_col)
        self.planned_text = QTextEdit(right_col)
        self.planned_text.setReadOnly(True)
        self.planned_text.setPlainText("Changes you want to make:")

        current_label = QLabel("Current device state", right_col)
        self.current_state_text = QTextEdit(right_col)
        self.current_state_text.setReadOnly(True)
        self.current_state_text.setPlainText("Not loaded yet.")

        buttons_row = QWidget(right_col)
        buttons_layout = QHBoxLayout(buttons_row)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(8)

        self.plan_btn = QPushButton("Plan to apply", buttons_row)
        self.confirm_btn = QPushButton("Confirm changes", buttons_row)
        self.cancel_btn = QPushButton("Cancel", buttons_row)

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
