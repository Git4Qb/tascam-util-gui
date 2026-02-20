# gui/layout/left_column.py

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

from core.device_state import DeviceState

from gui.tabs.routing_tab import RoutingTab
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
        self.routing_tab = RoutingTab(self)
        self.routing_tab.route_changed.connect(self.route_changed.emit)
        self.tabs.add_tab(self.routing_tab, "Routing")

        # Monitoring
        self.monitoring_tab = MonitoringTab(self)
        self.monitoring_tab.monitor_changed.connect(self.monitor_changed.emit)
        self.tabs.add_tab(self.monitoring_tab, "Monitoring")

        # Inputs
        self.inputs_tab = InputsTab(self)
        self.inputs_tab.input_changed.connect(self.input_changed.emit)
        self.tabs.add_tab(self.inputs_tab, "Inputs")

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

    def set_from_device_state(self, s: DeviceState) -> None:
        # IMPORTANT: block signals so loading state doesn't create "planned" edits.
        self.powersave_toggle.blockSignals(True)
        self.powersave_toggle.setChecked(bool(s.powersave))
        self.powersave_toggle.blockSignals(False)

        # Call optional tab APIs if they exist (won't crash if not implemented yet).
        if hasattr(self.inputs_tab, "set_from_device_state"):
            self.inputs_tab.set_from_device_state(s)
        elif hasattr(self.inputs_tab, "set_enabled_states"):
            self.inputs_tab.set_enabled_states(s.input_enable)

        if hasattr(self.monitoring_tab, "set_from_device_state"):
            self.monitoring_tab.set_from_device_state(s)
        elif hasattr(self.monitoring_tab, "set_modes"):
            self.monitoring_tab.set_modes(s.monitoring_mode)

        if hasattr(self.routing_tab, "set_from_device_state"):
            self.routing_tab.set_from_device_state(s)
        elif hasattr(self.routing_tab, "set_routes"):
            self.routing_tab.set_routes(s.routing)