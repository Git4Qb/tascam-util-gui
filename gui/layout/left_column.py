from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from gui.tabs.routing_tab import RoutingTab, RouteSelection
from gui.tabs.monitoring_tab import MonitoringTab
from gui.tabs.inputs_tab import InputsTab

from gui.widgets.tabs_panel import TabsPanel


class LeftColumnWidget(QWidget):
    """Dumb UI: tabs + powersave panel. Emits UI signals upward."""

    route_changed = Signal(object)          # RouteSelection
    monitor_changed = Signal(str, str)      # inp, mode
    input_changed = Signal(str, str)        # inp, mode
    powersave_toggled = Signal(bool)        # enabled

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.tabs = TabsPanel(self)

        # Routing
        routing = RoutingTab(self)
        routing.route_changed.connect(self.route_changed.emit)
        self.tabs.add_tab(routing, "Routing")

        # Monitoring
        monitoring = MonitoringTab(self)
        monitoring.monitor_changed.connect(self.monitor_changed.emit)
        self.tabs.add_tab(monitoring, "Monitoring")

        # Inputs
        inputs = InputsTab(self)
        inputs.input_changed.connect(self.input_changed.emit)
        self.tabs.add_tab(inputs, "Inputs")

        separator = QFrame(self)
        separator.setProperty("role", "sectionSeparator")
        separator.setFrameShape(QFrame.Shape.HLine)

        # PowerSave panel
        self.powersave_panel = QFrame(self)
        powersave_layout = QHBoxLayout(self.powersave_panel)
        powersave_layout.setContentsMargins(8, 6, 8, 6)
        powersave_layout.setSpacing(8)

        powersave_title = QLabel("PowerSave", self.powersave_panel)
        powersave_title.setProperty("role", "heading")

        powersave_enabled = QLabel("Enabled", self.powersave_panel)
        powersave_enabled.setProperty("role", "heading")

        self.powersave_toggle = QCheckBox(self.powersave_panel)
        self.powersave_toggle.setChecked(False)
        self.powersave_toggle.toggled.connect(self.powersave_toggled.emit)

        powersave_layout.addWidget(powersave_title)
        powersave_layout.addStretch(1)
        powersave_layout.addWidget(powersave_enabled)
        powersave_layout.addWidget(self.powersave_toggle)

        layout.addWidget(self.tabs, 1)
        layout.addWidget(separator, 0)
        layout.addWidget(self.powersave_panel, 0)

    def set_editable(self, enabled: bool) -> None:
        self.tabs.setEnabled(enabled)
        self.powersave_panel.setEnabled(enabled)

    def min_width_for_titles(self) -> int:
        return self.tabs.min_width_for_titles()