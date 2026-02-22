# gui/tabs/monitoring_tab.py

from __future__ import annotations

from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
QGridLayout,
QFrame,
QLabel,
QVBoxLayout,
QWidget,
QRadioButton,
QButtonGroup
)

from core.device_parameters import MonitoringPair, MonitoringMode
from core.device_state import DeviceState


class MonitoringTab(QWidget):
    """
    UI-only monitoring controls.
    Emits monitor_changed(pair: MonitoringPair, mode: MonitoringMode).
    """
    monitor_changed = Signal(object, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self) -> None:
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
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

        grid.addWidget(QLabel(card), 0, 0)

        h_mono = QLabel("MONO", card)
        h_stereo = QLabel("STEREO", card)
        h_mono.setProperty("role", "muted")
        h_stereo.setProperty("role", "muted")

        grid.addWidget(h_mono, 0, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(h_stereo, 0, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Inputs 1/2 row
        grid.addWidget(QLabel("Inputs 1/2", card), 1, 0)
        self.in12_mono = QRadioButton(card)
        self.in12_stereo = QRadioButton(card)
        grid.addWidget(self.in12_mono, 1, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.in12_stereo, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.grp_in12 = QButtonGroup(self)
        self.grp_in12.setExclusive(True)
        self.grp_in12.addButton(self.in12_mono)
        self.grp_in12.addButton(self.in12_stereo)

        self.in12_mono.toggled.connect(lambda checked: self._emit_if_checked(MonitoringPair.IN12, MonitoringMode.MONO, checked))
        self.in12_stereo.toggled.connect(lambda checked: self._emit_if_checked(MonitoringPair.IN12, MonitoringMode.STEREO, checked))

        # Inputs 3/4 row
        grid.addWidget(QLabel("Inputs 3/4", card), 2, 0)
        self.in34_mono = QRadioButton(card)
        self.in34_stereo = QRadioButton(card)
        grid.addWidget(self.in34_mono, 2, 1, alignment=Qt.AlignmentFlag.AlignHCenter)
        grid.addWidget(self.in34_stereo, 2, 2, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.grp_in34 = QButtonGroup(self)
        self.grp_in34.setExclusive(True)
        self.grp_in34.addButton(self.in34_mono)
        self.grp_in34.addButton(self.in34_stereo)

        self.in34_mono.toggled.connect(lambda checked: self._emit_if_checked(MonitoringPair.IN34, MonitoringMode.MONO, checked))
        self.in34_stereo.toggled.connect(lambda checked: self._emit_if_checked(MonitoringPair.IN34, MonitoringMode.STEREO, checked))

        card_layout.addLayout(grid)
        page_layout.addWidget(card)
        page_layout.addStretch(1)

        self.set_state(in12=MonitoringMode.STEREO, in34=MonitoringMode.STEREO, emit=False)

    def _emit_if_checked(self, pair: MonitoringPair, mode: MonitoringMode, checked: bool) -> None:
        if checked:
            self.monitor_changed.emit(pair, mode)

    def get_modes(self) -> dict[MonitoringPair, MonitoringMode]:
        return {
            MonitoringPair.IN12: MonitoringMode.MONO if self.in12_mono.isChecked() else MonitoringMode.STEREO,
            MonitoringPair.IN34: MonitoringMode.MONO if self.in34_mono.isChecked() else MonitoringMode.STEREO,
        }

    def set_state(self, *, in12: MonitoringMode, in34: MonitoringMode, emit: bool = False) -> None:
        radios = [self.in12_mono, self.in12_stereo, self.in34_mono, self.in34_stereo]
        if not emit:
            for r in radios:
                r.blockSignals(True)

        self.in12_mono.setChecked(in12 == MonitoringMode.MONO)
        self.in12_stereo.setChecked(in12 == MonitoringMode.STEREO)
        self.in34_mono.setChecked(in34 == MonitoringMode.MONO)
        self.in34_stereo.setChecked(in34 == MonitoringMode.STEREO)

        if not emit:
            for r in radios:
                r.blockSignals(False)

    def set_from_device_state(self, s: DeviceState) -> None:
        # s.monitoring_mode is [0..1] where enum matches MonitoringMode
        in12 = MonitoringMode(int(s.monitoring_mode[0])) if len(s.monitoring_mode) > 0 else MonitoringMode.STEREO
        in34 = MonitoringMode(int(s.monitoring_mode[1])) if len(s.monitoring_mode) > 1 else MonitoringMode.STEREO
        self.set_state(in12=in12, in34=in34, emit=False)