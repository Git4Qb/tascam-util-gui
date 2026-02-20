from __future__ import annotations

import json
import sys
from pathlib import Path

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from core.devices import SUPPORTED_DEVICES
from core.detector import detect_supported_devices
from core.device_manager import DeviceManager

from gui.layout.left_column import LeftColumnWidget
from gui.layout.right_column import RightColumnWidget
from gui.layout.status_bar import StatusBarWidget

from gui.widgets.planned_changes import PlannedChanges
from gui.widgets.planned_keys import PLANNED_ORDER
from gui.widgets.ui_text import MONITORING_INPUT_LABELS, ROUTING_SOURCE_LABELS

from gui.tabs.routing_tab import RouteSelection


class MainWindow(QMainWindow):
    """Controller: owns state, connects signals, manages modes, profiles, autodetect."""

    PROFILE_DIRNAME = "profiles"
    PROFILE_FILENAME = "device_profiles.json"

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("TASCAMUS 4x4")
        self.resize(980, 720)

        self.device_manager: DeviceManager | None = None
        self._planned = PlannedChanges(order=PLANNED_ORDER)

        root = QWidget(self)
        self.setCentralWidget(root)

        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(10)

        content_row = QWidget(root)
        content_layout = QHBoxLayout(content_row)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(12)

        self.left = LeftColumnWidget(content_row)
        self.right = RightColumnWidget(content_row)
        self.status = StatusBarWidget(root)

        content_layout.addWidget(self.left, 3)
        content_layout.addWidget(self.right, 2)

        root_layout.addWidget(content_row, 1)
        root_layout.addWidget(self.status, 0)

        # Wire UI → controller
        self.left.route_changed.connect(self._on_route_changed)
        self.left.monitor_changed.connect(self._on_monitor_changed)
        self.left.input_changed.connect(self._on_input_changed)
        self.left.powersave_toggled.connect(self._on_powersave_toggled)

        self.right.plan_clicked.connect(self._set_planned_mode)
        self.right.cancel_clicked.connect(self._set_editing_mode)
        # confirm_clicked stays for later (apply-to-device)
        # self.right.confirm_clicked.connect(self._on_confirm_clicked)

        self.status.reconnect_clicked.connect(self._on_reconnect_clicked)
        self.status.save_profile_clicked.connect(self._on_save_profile_clicked)
        self.status.load_profile_clicked.connect(self._on_load_profile_clicked)

        # Initial UI state
        self._render_planned()
        self._set_idle_mode()
        self._set_status("No device connected.", can_reconnect=True)

        QTimer.singleShot(0, self._apply_min_window_width)
        QTimer.singleShot(0, self._startup_autodetect)

    # -------------------------
    # Profiles
    # -------------------------

    def _profiles_path(self) -> Path:
        base = Path(__file__).resolve().parent
        d = base / self.PROFILE_DIRNAME
        d.mkdir(parents=True, exist_ok=True)
        return d / self.PROFILE_FILENAME

    def _load_profiles(self) -> dict:
        path = self._profiles_path()
        if not path.exists():
            return {"devices": {}}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {"devices": {}}

    def _save_profiles(self, data: dict) -> None:
        self._profiles_path().write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _device_key(self) -> str:
        if self.device_manager is not None:
            desc = getattr(self.device_manager, "descriptor", None)
            if desc is not None:
                return f"{desc.vendor_id:04x}:{desc.product_id:04x}"
        return "offline"

    def _device_display_name(self) -> str:
        if self.device_manager is not None:
            desc = getattr(self.device_manager, "descriptor", None)
            if desc is not None:
                return desc.name
        return "No device"

    def _on_save_profile_clicked(self) -> None:
        if self.device_manager is None or not getattr(self.device_manager, "connected", False):
            QMessageBox.information(self, "Save profile", "Connect a device first, then save a profile for it.")
            return

        name, ok = QInputDialog.getText(self, "Save profile", f"Profile name for {self._device_display_name()}:")
        if not ok:
            return
        name = name.strip()
        if not name:
            return

        data = self._load_profiles()
        devices = data.setdefault("devices", {})
        key = self._device_key()
        dev = devices.setdefault(key, {"profiles": {}})
        dev["profiles"][name] = {"planned_lines": dict(self._planned.lines)}
        self._save_profiles(data)

        self._set_status(f"Saved profile '{name}' for {self._device_display_name()}.", can_reconnect=True)

    def _on_load_profile_clicked(self) -> None:
        if self.device_manager is None or not getattr(self.device_manager, "connected", False):
            QMessageBox.information(self, "Load profile", "Connect a device first, then load a profile for it.")
            return

        data = self._load_profiles()
        devices = data.get("devices", {})
        dev = devices.get(self._device_key())
        profiles = (dev or {}).get("profiles", {})
        if not profiles:
            QMessageBox.information(self, "Load profile", f"No saved profiles found for {self._device_display_name()}.")
            return

        labels = sorted(profiles.keys())
        choice, ok = QInputDialog.getItem(
            self, "Load profile", f"Select a profile for {self._device_display_name()}:", labels, 0, False
        )
        if not ok:
            return

        payload = profiles.get(choice, {})
        planned_lines = payload.get("planned_lines", {})

        self._planned.clear()
        for k, v in planned_lines.items():
            self._planned.set_line(k, v)
        self._render_planned()

        self._set_status(f"Loaded profile '{choice}' for {self._device_display_name()}.", can_reconnect=True)

    # -------------------------
    # Device autodetect
    # -------------------------

    def _startup_autodetect(self) -> None:
        devices = detect_supported_devices(SUPPORTED_DEVICES)

        if len(devices) == 0:
            self.device_manager = None
            self._set_idle_mode()
            self._set_status("No supported device detected.", can_reconnect=True)
            return

        if len(devices) == 1:
            selected = devices[0]
            dm = DeviceManager(selected)
            if dm.connect():
                self.device_manager = dm
                self._set_editing_mode()
                self._set_status(f"Connected: {selected.name}", can_reconnect=True)
                return

            self.device_manager = None
            self._set_idle_mode()
            self._set_status("Connection failed.", can_reconnect=True)
            return

        labels = [d.name for d in devices]
        choice, ok = QInputDialog.getItem(
            self, "Select device", "Multiple supported devices detected. Choose one.", labels, 0, False
        )
        if not ok:
            self.device_manager = None
            self._set_idle_mode()
            self._set_status("Device selection canceled.", can_reconnect=True)
            return

        selected = devices[labels.index(choice)]
        dm = DeviceManager(selected)
        if dm.connect():
            self.device_manager = dm
            self._set_editing_mode()
            self._set_status(f"Connected: {selected.name}", can_reconnect=True)
        else:
            self.device_manager = None
            self._set_idle_mode()
            err = dm.last_error or "Unknown error"
            self._set_status(f"Connection failed: {err}", can_reconnect=True)
            return

        self.device_manager = None
        self._set_idle_mode()
        self._set_status("Connection failed.", can_reconnect=True)

    # -------------------------
    # Reconnect modal logic
    # -------------------------

    def _on_reconnect_clicked(self) -> None:
        if self.device_manager is None or not getattr(self.device_manager, "connected", False):
            self._startup_autodetect()
            return

        dev_name = self._device_display_name()

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Reconnect device?")
        msg.setText(f"{dev_name} is currently connected.")
        msg.setInformativeText(
            "Abort current connection?\n"
            "All planned (not confirmed) changes will be cleared.\n"
            "Save a profile first if you want to keep them."
        )

        cancel_btn = msg.addButton("Cancel", QMessageBox.ButtonRole.RejectRole)
        abort_btn = msg.addButton("Abort connection", QMessageBox.ButtonRole.DestructiveRole)
        msg.setDefaultButton(cancel_btn)

        msg.exec()

        if msg.clickedButton() is abort_btn:
            self._abort_connection_and_redetect()

    def _abort_connection_and_redetect(self) -> None:
        if self.device_manager is not None:
            try:
                if hasattr(self.device_manager, "disconnect"):
                    self.device_manager.disconnect()
            except Exception:
                pass

        self.device_manager = None

        self._planned.clear()
        self._render_planned()

        self._set_idle_mode()
        self._set_status("Disconnected. Ready to reconnect.", can_reconnect=True)

        self._startup_autodetect()

    # -------------------------
    # Planned rendering
    # -------------------------

    def _render_planned(self) -> None:
        self.right.set_planned_text(self._planned.render())

    def _set_planned_line(self, key: str, text: str) -> None:
        self._planned.set_line(key, text)
        self._render_planned()

    # -------------------------
    # UI handlers (UI-only)
    # -------------------------

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

    # -------------------------
    # Modes
    # -------------------------

    def _set_editing_mode(self) -> None:
        self.left.set_editable(True)
        self.right.set_buttons(plan=True, confirm=False, cancel=False)
        self.status.set_profiles_enabled(True)

    def _set_planned_mode(self) -> None:
        self.left.set_editable(False)
        self.right.set_buttons(plan=False, confirm=True, cancel=True)
        self.status.set_profiles_enabled(True)

    def _set_idle_mode(self) -> None:
        self.left.set_editable(False)
        self.right.set_buttons(plan=False, confirm=False, cancel=False)
        self.status.set_profiles_enabled(False)

    # -------------------------
    # Status + sizing
    # -------------------------

    def _set_status(self, text: str, *, can_reconnect: bool = True) -> None:
        self.status.set_status(text)
        self.status.set_reconnect_enabled(can_reconnect)

    def _apply_min_window_width(self) -> None:
        tabs_min = self.left.min_width_for_titles()
        right_min = self.right.minimumSizeHint().width()

        layout = self.centralWidget().layout()
        margins = layout.contentsMargins()

        total = margins.left() + margins.right() + 12 + tabs_min + right_min
        self.setMinimumWidth(total)


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