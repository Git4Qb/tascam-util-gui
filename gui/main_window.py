from PySide6.QtWidgets import QMainWindow, QTabWidget

from gui.tabs import RoutingTab, MonitoringTab, InputsTab, PowerSaveTab


class MainWindow(QMainWindow):
    """Main window with top-level tabs only."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("TASCAM Utility")
        self.resize(900, 600)

        tabs = QTabWidget(self)
        tabs.addTab(RoutingTab(), "Routing")
        tabs.addTab(MonitoringTab(), "Monitoring")
        tabs.addTab(InputsTab(), "Inputs")
        tabs.addTab(PowerSaveTab(), "PowerSave")

        self.setCentralWidget(tabs)
