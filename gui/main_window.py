# gui/main_window.py
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
from core.device_state import DeviceState

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
        self.right.confirm_clicked.connect(self._on_confirm_clicked)

        self.status.reconnect_clicked.connect(self._on_reconnect_clicked)
        self.status.save_profile_clicked.connect(self._on_save_profile_clicked)
        self.status.load_profile_clicked.connect(self._on_load_profile_clicked)

        # Initial UI state
        self._render_planned()
        self._set_idle_mode()
        self._set_status("No device connected.", can_reconnect=True)
        self.right.set_current_state_text("Not loaded yet.")

        QTimer.singleShot(0, self._apply_min_window_width)
        QTimer.singleShot(0, self._startup_autodetect)



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
            self.right.set_current_state_text("Not loaded yet.")
            self._set_status("No supported device detected.", can_reconnect=True)
            return

        if len(devices) == 1:
            selected = devices[0]
            dm = DeviceManager(selected)
            self._connect_and_load_state(dm, selected.name)
            return

        labels = [d.name for d in devices]
        choice, ok = QInputDialog.getItem(
            self,
            "Select device",
            "Multiple supported devices detected. Choose one.",
            labels,
            0,
            False,
        )
        if not ok:
            self.device_manager = None
            self._set_idle_mode()
            self.right.set_current_state_text("Not loaded yet.")
            self._set_status("Device selection canceled.", can_reconnect=True)
            return

        selected = devices[labels.index(choice)]
        dm = DeviceManager(selected)
        self._connect_and_load_state(dm, selected.name)

    def _connect_and_load_state(self, dm: DeviceManager, device_name: str) -> None:
        if dm.connect():
            self.device_manager = dm
            self._set_editing_mode()
            self._set_status(f"Connected: {device_name}", can_reconnect=True)

            state = dm.read_state()
            if state is not None:
                self._apply_device_state_to_gui(state)
            else:
                err = dm.last_error or "Unknown error"
                self.right.set_current_state_text(f"State read failed: {err}")

            return

        # connect failed
        self.device_manager = None
        self._set_idle_mode()
        self.right.set_current_state_text("Not loaded yet.")
        err = dm.last_error or "Unknown error"
        self._set_status(f"Connection failed: {err}", can_reconnect=True)

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
        self.right.set_current_state_text("Not loaded yet.")
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

    # -------------------------
    # DeviceState -> UI
    # -------------------------

    def _format_device_state(self, s: DeviceState) -> str:
        ps = "On" if s.powersave else "Off"

        inputs = ", ".join(
            f"IN{i + 1}={'On' if enabled else 'Off'}"
            for i, enabled in enumerate(s.input_enable)
        )

        mon = ", ".join(
            f"IN{pair}={'Stereo' if mode == 1 else 'Mono'}"
            for pair, mode in zip(("1/2", "3/4"), s.monitoring_mode)
        )

        rout = ", ".join(
            f"Line {pair}={val}"
            for pair, val in zip(("1/2", "3/4"), s.routing)
        )

        return "\n".join([
            f"PowerSave: {ps}",
            f"Inputs: {inputs}",
            f"Monitoring: {mon}",
            f"Routing: {rout}",
        ])

    def _apply_device_state_to_gui(self, state: DeviceState) -> None:
        self.right.set_current_state_text(self._format_device_state(state))
        self.left.set_from_device_state(state)

    def _device_set_powersave(self, enabled: bool) -> None:
        """
        Uses DeviceManager API if it exists, otherwise falls back to protocol.
        """
        dm = self.device_manager
        if dm is None:
            return

        if hasattr(dm, "set_powersave"):
            dm.set_powersave(enabled)
            return

        # fallback: direct protocol call if DeviceManager doesn’t wrap it
        from core import protocol
        protocol.write_byte(dm.transport, protocol.COMMAND_POWERSAVE, 0, 1 if enabled else 0)

    def _device_set_input_enable(self, input_num: int, enabled: bool) -> None:
        dm = self.device_manager
        if dm is None:
            return

        idx = input_num - 1  # IN1->0
        if hasattr(dm, "set_input_enable"):
            dm.set_input_enable(idx, enabled)
            return

        from core import protocol
        protocol.write_byte(dm.transport, protocol.COMMAND_INPUT_ENABLE, idx, 1 if enabled else 0)

    def _device_set_monitoring(self, pair: str, mono: bool) -> None:
        dm = self.device_manager
        if dm is None:
            return

        idx = 0 if pair == "IN12" else 1
        value = 0 if mono else 1

        if hasattr(dm, "set_monitoring_mode"):
            dm.set_monitoring_mode(idx, value)
            return

        from core import protocol
        protocol.write_byte(dm.transport, protocol.COMMAND_MONITORING_MODE, idx, value)

    def _device_set_routing(self, dest: str, source: str) -> None:
        dm = self.device_manager
        if dm is None:
            return

        idx = 0 if dest == "LINE12" else 1
        src_to_val = {"MIX": 0, "OUT12": 1, "OUT34": 2}
        value = src_to_val.get(source, 0)

        if hasattr(dm, "set_routing"):
            dm.set_routing(idx, value)
            return

        from core import protocol
        protocol.write_byte(dm.transport, protocol.COMMAND_ROUTING, idx, value)


    def _on_confirm_clicked(self) -> None:
        """
        Apply planned changes to device, then re-read state and clear plan.
        """
        if self.device_manager is None or not getattr(self.device_manager, "connected", False):
            self._set_status("No device connected.", can_reconnect=True)
            return

        # 1) Apply plan to device
        try:
            self._apply_planned_changes_to_device()
        except Exception as e:
            self._set_status(f"Apply failed: {e}", can_reconnect=True)
            return

        # 2) Clear plan + back to editing
        self._planned.clear()
        self._render_planned()
        self._set_editing_mode()
        self._set_status("Applied changes.", can_reconnect=True)

        # 3) Refresh device state (truth)
        state = self.device_manager.read_state()
        if state is not None:
            self._apply_device_state_to_gui(state)


    def _apply_planned_changes_to_device(self) -> None:
        """
        Translate PlannedChanges.lines into actual device commands.
        """
        dm = self.device_manager
        if dm is None:
            return

        lines = dict(self._planned.lines)

        # --- PowerSave ---
        # Your planned line looks like: "PowerSave: ON|OFF"
        if "POWERSAVE" in lines:
            enabled = "ON" in lines["POWERSAVE"].upper()
            self._device_set_powersave(enabled)

        # --- Inputs ---
        # Planned keys: IN1..IN4
        for i in range(1, 5):
            key = f"IN{i}"
            if key in lines:
                enabled = "ON" in lines[key].upper()
                self._device_set_input_enable(i, enabled)

        # --- Monitoring ---
        # Keys: IN12 / IN34 (from MonitoringTab signal)
        if "IN12" in lines:
            mono = "MONO" in lines["IN12"].upper()
            self._device_set_monitoring("IN12", mono)

        if "IN34" in lines:
            mono = "MONO" in lines["IN34"].upper()
            self._device_set_monitoring("IN34", mono)

        # --- Routing ---
        # Keys: LINE12 / LINE34
        if "LINE12" in lines:
            src = self._extract_routing_source(lines["LINE12"])
            self._device_set_routing("LINE12", src)

        if "LINE34" in lines:
            src = self._extract_routing_source(lines["LINE34"])
            self._device_set_routing("LINE34", src)


    def _extract_routing_source(self, planned_text: str) -> str:
        """
        planned_text example: "Routing Line 1/2: Monitor Mix"
        Return: "MIX" | "OUT12" | "OUT34"
        """
        t = planned_text.upper()
        if "MONITOR MIX" in t:
            return "MIX"
        if "OUT 1/2" in t or "1/2" in t and "COMPUTER" in t:
            return "OUT12"
        if "OUT 3/4" in t or "3/4" in t and "COMPUTER" in t:
            return "OUT34"
        # safe default
        return "MIX"




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