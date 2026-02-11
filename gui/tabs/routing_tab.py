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


ARROW = "→"


@dataclass(frozen=True)
class RouteSelection:
    dest: str    # LINE12 / LINE34
    source: str  # MIX / OUT12 / OUT34


class RoutingTab(QWidget):
    """
    GUI representation of:

        route -s {MIX|OUT12|OUT34} -d {LINE12|LINE34}

    This class does NOT execute commands.
    It only stores and exposes routing state.
    """

    route_changed = Signal(object)  # emits RouteSelection

    SOURCES = [
        ("MIX", "MIX"),
        ("Out 1/2", "OUT12"),
        ("Out 3/4", "OUT34"),
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

        # --- LINE 1/2 ---
        grid.addWidget(QLabel("Line 1/2", card), 0, 0)
        self.combo_line12 = self._make_source_combo(card)
        grid.addWidget(self.combo_line12, 0, 1)

        # --- LINE 3/4 ---
        grid.addWidget(QLabel("Line 3/4", card), 1, 0)
        self.combo_line34 = self._make_source_combo(card)
        grid.addWidget(self.combo_line34, 1, 1)

        grid.setColumnStretch(2, 1)

        layout.addWidget(heading)
        layout.addWidget(card)
        layout.addStretch(1)

        # Default values
        self.set_route("LINE12", "MIX")
        self.set_route("LINE34", "MIX")

        # Signals
        self.combo_line12.currentIndexChanged.connect(
            lambda _: self._emit_change("LINE12")
        )
        self.combo_line34.currentIndexChanged.connect(
            lambda _: self._emit_change("LINE34")
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _make_source_combo(self, parent: QWidget) -> QComboBox:
        combo = QComboBox(parent)
        for label, value in self.SOURCES:
            combo.addItem(label, value)
        return combo

    def _emit_change(self, dest: str) -> None:
        self.route_changed.emit(
            RouteSelection(dest=dest, source=self.route_for(dest))
        )

    # ------------------------------------------------------------------
    # Public API (state access)
    # ------------------------------------------------------------------

    def route_for(self, dest: str) -> str:
        if dest == "LINE12":
            return str(self.combo_line12.currentData())
        if dest == "LINE34":
            return str(self.combo_line34.currentData())
        raise ValueError(f"Unknown dest: {dest}")

    def set_route(self, dest: str, source: str) -> None:
        if dest == "LINE12":
            combo = self.combo_line12
        elif dest == "LINE34":
            combo = self.combo_line34
        else:
            raise ValueError(f"Unknown dest: {dest}")

        idx = combo.findData(source)
        if idx >= 0:
            combo.setCurrentIndex(idx)
        else:
            raise ValueError(f"Unknown source: {source}")

    def get_routes(self) -> dict[str, str]:
        """
        Returns:
            {
                "LINE12": "MIX" | "OUT12" | "OUT34",
                "LINE34": "MIX" | "OUT12" | "OUT34"
            }
        """
        return {
            "LINE12": self.route_for("LINE12"),
            "LINE34": self.route_for("LINE34"),
        }

    # ------------------------------------------------------------------
    # Human-readable plan
    # ------------------------------------------------------------------

    def planned_human_readable(self) -> list[str]:
        routes = self.get_routes()

        source_map = {
            "MIX": "Monitor Mix",
            "OUT12": "Computer Out 1/2",
            "OUT34": "Computer Out 3/4",
        }

        return [
            f"{source_map[routes['LINE12']]} {ARROW} US-4x4 Line 1/2",
            f"{source_map[routes['LINE34']]} {ARROW} US-4x4 Line 3/4",
        ]
