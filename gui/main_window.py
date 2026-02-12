# gui/main_window.py
"""Main GUI window layout for TASCAMUS 4x4.

This module contains only GUI scaffolding/state behavior.
No device/core command logic is invoked here.
"""
from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .widgets.tabs_panel import TabsPanel
from .widgets.planned_changes import PlannedChanges
from .widgets.ui_text import MONITORING_INPUT_LABELS, ROUTING_SOURCE_LABELS
from .widgets.planned_keys import PLANNED_ORDER

from gui.tabs.routing_tab import RoutingTab, RouteSelection
from gui.tabs.monitoring_tab import MonitoringTab
from gui.tabs.inputs_tab import InputsTab



class MainWindow(QMainWindow):
    """Main window with left settings column and right planning/status column."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("TASCAMUS 4x4")
        self.resize(980, 720)

        # Planned changes model (keeps summary lines)
        self._planned = PlannedChanges(order=PLANNED_ORDER)

        root = QWidget(self)
        self.setCentralWidget(root)

        main_layout = QHBoxLayout(root)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # Right is first so planned_text exists before left wires signals
        right = self._build_right_column()
        left = self._build_left_column()

        main_layout.addWidget(left, 3)
        main_layout.addWidget(right, 2)

        self._render_planned()
        self._set_editing_mode()
        QTimer.singleShot(0, self._apply_min_window_width)

    # ------------------------------------------------------------------
    # Planned changes helpers
    # ------------------------------------------------------------------

    def _set_planned_line(self, key: str, text: str) -> None:
        self._planned.set_line(key, text)
        self._render_planned()

    def _render_planned(self) -> None:
        self.planned_text.setPlainText(self._planned.render())

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _apply_min_window_width(self) -> None:
        tabs_min = self.tabs.min_width_for_titles()
        right_min = self._right_col.minimumSizeHint().width()

        layout = self.centralWidget().layout()
        margins = layout.contentsMargins()
        spacing = layout.spacing()

        total = margins.left() + margins.right() + spacing + tabs_min + right_min
        self.setMinimumWidth(total)

    def _build_left_column(self) -> QWidget:
        left_col = QWidget(self)
        left_layout = QVBoxLayout(left_col)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)

        self.tabs = TabsPanel(left_col)

        # --- Routing ---
        routing = RoutingTab(left_col)
        routing.route_changed.connect(self._on_route_changed)
        self.tabs.add_tab(routing, "Routing")

        # --- Monitoring ---
        monitoring = MonitoringTab(left_col)
        monitoring.monitor_changed.connect(self._on_monitor_changed)
        self.tabs.add_tab(monitoring, "Monitoring")

        # --- Inputs ---
        inputs = InputsTab(left_col)
        inputs.input_changed.connect(self._on_input_changed)
        self.tabs.add_tab(inputs, "Inputs")

        separator = QFrame(left_col)
        separator.setProperty("role", "sectionSeparator")
        separator.setFrameShape(QFrame.Shape.HLine)

        # --- PowerSave panel ---
        self.powersave_panel = QFrame(left_col)
        powersave_layout = QHBoxLayout(self.powersave_panel)
        powersave_layout.setContentsMargins(8, 6, 8, 6)
        powersave_layout.setSpacing(8)

        powersave_title = QLabel("PowerSave", self.powersave_panel)
        powersave_title.setProperty("role", "heading")

        powersave_enabled = QLabel("Enabled", self.powersave_panel)
        powersave_enabled.setProperty("role", "heading")

        self.powersave_toggle = QCheckBox(self.powersave_panel)
        self.powersave_toggle.setChecked(False)
        self.powersave_toggle.toggled.connect(self._on_powersave_toggled)

        powersave_layout.addWidget(powersave_title)
        powersave_layout.addStretch(1)
        powersave_layout.addWidget(powersave_enabled)
        powersave_layout.addWidget(self.powersave_toggle)

        left_layout.addWidget(self.tabs, 1)
        left_layout.addWidget(separator, 0)
        left_layout.addWidget(self.powersave_panel, 0)

        return left_col

    def _build_right_column(self) -> QWidget:
        right_col = QWidget(self)
        self._right_col = right_col

        right_layout = QVBoxLayout(right_col)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        planned_label = QLabel("Planned changes", right_col)
        self.planned_text = QTextEdit(right_col)
        self.planned_text.setReadOnly(True)

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

        self.plan_btn.clicked.connect(self._set_planned_mode)
        self.cancel_btn.clicked.connect(self._set_editing_mode)

        buttons_layout.addWidget(self.plan_btn)
        buttons_layout.addWidget(self.confirm_btn)
        buttons_layout.addWidget(self.cancel_btn)

        right_layout.addWidget(planned_label, 0)
        right_layout.addWidget(self.planned_text, 1)
        right_layout.addWidget(current_label, 0)
        right_layout.addWidget(self.current_state_text, 1)
        right_layout.addWidget(buttons_row, 0)

        return right_col

    # ------------------------------------------------------------------
    # Signal handlers (UI-only)
    # ------------------------------------------------------------------

    def _on_monitor_changed(self, inp: str, mode: str) -> None:
        label = MONITORING_INPUT_LABELS.get(inp, inp)
        self._set_planned_line(inp, f"Monitoring {label}: {mode}")

    def _on_route_changed(self, sel: RouteSelection) -> None:
        source_label = ROUTING_SOURCE_LABELS.get(sel.source, sel.source)
        if sel.dest == "LINE12":
            self._set_planned_line("LINE12", f"Routing Line 1/2: {source_label}")
        elif sel.dest == "LINE34":
            self._set_planned_line("LINE34", f"Routing Line 3/4: {source_label}")

    def _on_input_changed(self, inp: str, mode: str) -> None:
        self._set_planned_line(inp, f"Input {inp}: {mode}")

    def _on_powersave_toggled(self, enabled: bool) -> None:
        mode = "ON" if enabled else "OFF"
        self._set_planned_line("POWERSAVE", f"PowerSave: {mode}")

    # ------------------------------------------------------------------
    # Modes
    # ------------------------------------------------------------------

    def _set_editing_mode(self) -> None:
        self.tabs.setEnabled(True)
        self.powersave_panel.setEnabled(True)
        self.plan_btn.setEnabled(True)
        self.confirm_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)

    def _set_planned_mode(self) -> None:
        self.tabs.setEnabled(False)
        self.powersave_panel.setEnabled(False)
        self.plan_btn.setEnabled(False)
        self.confirm_btn.setEnabled(True)
        self.cancel_btn.setEnabled(True)


def main() -> int:
    app = QApplication(sys.argv)

    qss = Path(__file__).with_name("style.qss")
    if qss.exists():
        app.setStyleSheet(qss.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
