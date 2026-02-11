# gui/tabs/monitoring_tab.py

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QGridLayout,
    QRadioButton,
    QButtonGroup,
)


class MonitoringTab(QWidget):
    """
    GUI representation of:

        monitor -i {IN12|IN34} -m {MONO|STEREO}

    This class does NOT execute commands.
    It only stores and exposes monitoring state.
    """

    monitor_changed = Signal(str, str)  # ("IN12"/"IN34", "MONO"/"STEREO")

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(16, 16, 16, 16)
        page_layout.setSpacing(12)

        heading = QLabel("Monitoring", self)
        heading.setProperty("role", "heading")
        page_layout.addWidget(heading)

        card = QFrame(self)
        card.setProperty("role", "card")
        card.setFrameShape(QFrame.Shape.StyledPanel)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(12)

        subtitle = QLabel("Direct monitoring mode", card)
        subtitle.setProperty("role", "muted")
        card_layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(10)

        # --- Header row ---
        grid.addWidget(QLabel("", card), 0, 0)

        h_mono = QLabel("MONO", card)
        h_stereo = QLabel("STEREO", card)
        h_mono.setProperty("role", "muted")
        h_stereo.setProperty("role", "muted")

        grid.addWidget(
            h_mono, 0, 1,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        grid.addWidget(
            h_stereo, 0, 2,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

        # --- Row: Inputs 1/2 ---
        grid.addWidget(QLabel("Inputs 1/2", card), 1, 0)

        self.in12_mono = QRadioButton(card)
        self.in12_stereo = QRadioButton(card)

        grid.addWidget(
            self.in12_mono, 1, 1,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        grid.addWidget(
            self.in12_stereo, 1, 2,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

        self.grp_in12 = QButtonGroup(self)
        self.grp_in12.setExclusive(True)
        self.grp_in12.addButton(self.in12_mono)
        self.grp_in12.addButton(self.in12_stereo)

        self.in12_mono.toggled.connect(
            lambda checked: self._emit_if_checked("IN12", "MONO", checked)
        )
        self.in12_stereo.toggled.connect(
            lambda checked: self._emit_if_checked("IN12", "STEREO", checked)
        )

        # --- Row: Inputs 3/4 ---
        grid.addWidget(QLabel("Inputs 3/4", card), 2, 0)

        self.in34_mono = QRadioButton(card)
        self.in34_stereo = QRadioButton(card)

        grid.addWidget(
            self.in34_mono, 2, 1,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        grid.addWidget(
            self.in34_stereo, 2, 2,
            alignment=Qt.AlignmentFlag.AlignHCenter
        )

        self.grp_in34 = QButtonGroup(self)
        self.grp_in34.setExclusive(True)
        self.grp_in34.addButton(self.in34_mono)
        self.grp_in34.addButton(self.in34_stereo)

        self.in34_mono.toggled.connect(
            lambda checked: self._emit_if_checked("IN34", "MONO", checked)
        )
        self.in34_stereo.toggled.connect(
            lambda checked: self._emit_if_checked("IN34", "STEREO", checked)
        )

        card_layout.addLayout(grid)
        page_layout.addWidget(card)
        page_layout.addStretch(1)

        # Default state
        self.set_state(in12_mode="STEREO", in34_mode="STEREO", emit=False)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _emit_if_checked(self, input_name: str, mode_name: str, checked: bool) -> None:
        if checked:
            self.monitor_changed.emit(input_name, mode_name)

    # ------------------------------------------------------------------
    # Public API (state access)
    # ------------------------------------------------------------------

    def get_modes(self) -> dict[str, str]:
        return {
            "IN12": "MONO" if self.in12_mono.isChecked() else "STEREO",
            "IN34": "MONO" if self.in34_mono.isChecked() else "STEREO",
        }

    def set_state(
        self,
        *,
        in12_mode: str,
        in34_mode: str,
        emit: bool = False,
    ) -> None:

        radios = [
            self.in12_mono,
            self.in12_stereo,
            self.in34_mono,
            self.in34_stereo,
        ]

        if not emit:
            for r in radios:
                r.blockSignals(True)

        self.in12_mono.setChecked(in12_mode.upper() == "MONO")
        self.in12_stereo.setChecked(in12_mode.upper() == "STEREO")
        self.in34_mono.setChecked(in34_mode.upper() == "MONO")
        self.in34_stereo.setChecked(in34_mode.upper() == "STEREO")

        if not emit:
            for r in radios:
                r.blockSignals(False)
