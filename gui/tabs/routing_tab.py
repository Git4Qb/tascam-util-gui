# gui/tabs/routing_tab.py

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from core.device_parameters import RoutingDest, RoutingSource
from core.device_state import DeviceState


@dataclass(frozen=True)
class RouteSelection:
    dest: RoutingDest
    source: RoutingSource


class RoutingTab(QWidget):
    """
    UI-only routing controls.
    Emits route_changed(RouteSelection(dest: RoutingDest, source: RoutingSource))
    """

    route_changed = Signal(object)

    SOURCES = [
        ("Monitor Mix", RoutingSource.MONITOR_MIX),
        ("Computer Out 1/2", RoutingSource.PC_12),
        ("Computer Out 3/4", RoutingSource.PC_34),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        heading = QLabel("Routing", self)
        heading.setProperty("role", "heading")

        card = QFrame(self)
        card.setProperty("role", "card")

        grid = QGridLayout(card)
        grid.setContentsMargins(16, 16, 16, 16)
        grid.setHorizontalSpacing(14)
        grid.setVerticalSpacing(12)

        grid.addWidget(QLabel("Line 1/2", card), 0, 0)
        self.combo_line12 = self._make_source_combo(card)
        grid.addWidget(self.combo_line12, 0, 1)

        grid.addWidget(QLabel("Line 3/4", card), 1, 0)
        self.combo_line34 = self._make_source_combo(card)
        grid.addWidget(self.combo_line34, 1, 1)

        grid.setColumnStretch(2, 1)

        layout.addWidget(heading)
        layout.addWidget(card)
        layout.addStretch(1)

        # Defaults
        self.set_route(RoutingDest.LINE12, RoutingSource.MONITOR_MIX)
        self.set_route(RoutingDest.LINE34, RoutingSource.MONITOR_MIX)

        self.combo_line12.currentIndexChanged.connect(lambda _: self._emit_change(RoutingDest.LINE12))
        self.combo_line34.currentIndexChanged.connect(lambda _: self._emit_change(RoutingDest.LINE34))

    def _make_source_combo(self, parent: QWidget) -> QComboBox:
        combo = QComboBox(parent)
        for label, src in self.SOURCES:
            combo.addItem(label, src)  # store enum in userData
        return combo

    def _emit_change(self, dest: RoutingDest) -> None:
        self.route_changed.emit(RouteSelection(dest=dest, source=self.route_for(dest)))

    def route_for(self, dest: RoutingDest) -> RoutingSource:
        combo = self.combo_line12 if dest == RoutingDest.LINE12 else self.combo_line34
        data = combo.currentData()
        if not isinstance(data, RoutingSource):
            # defensive: if Qt gives int back in some edge-case
            return RoutingSource(int(data))
        return data

    def set_route(self, dest: RoutingDest, source: RoutingSource) -> None:
        combo = self.combo_line12 if dest == RoutingDest.LINE12 else self.combo_line34
        idx = combo.findData(source)
        if idx >= 0:
            combo.setCurrentIndex(idx)
        else:
            raise ValueError(f"Unknown source: {source}")

    def get_routes(self) -> dict[RoutingDest, RoutingSource]:
        return {
            RoutingDest.LINE12: self.route_for(RoutingDest.LINE12),
            RoutingDest.LINE34: self.route_for(RoutingDest.LINE34),
        }

    def set_from_device_state(self, s: DeviceState) -> None:
        line12 = RoutingSource(int(s.routing[0])) if len(s.routing) > 0 else RoutingSource.MONITOR_MIX
        line34 = RoutingSource(int(s.routing[1])) if len(s.routing) > 1 else RoutingSource.MONITOR_MIX

        self.combo_line12.blockSignals(True)
        self.combo_line34.blockSignals(True)
        try:
            self.set_route(RoutingDest.LINE12, line12)
            self.set_route(RoutingDest.LINE34, line34)
        finally:
            self.combo_line12.blockSignals(False)
            self.combo_line34.blockSignals(False)