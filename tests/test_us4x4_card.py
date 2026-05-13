from __future__ import annotations

import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from tuxam.devices.us_4x4.parameters import INPUT_CHANNEL, InputChannelState
from tuxam.ui.widgets.us4x4_card import US4x4Card


class RecordingUS4x4Driver:
    def __init__(
        self,
        confirmed_state: InputChannelState = InputChannelState.ON,
        error: Exception | None = None,
    ) -> None:
        self.confirmed_state = confirmed_state
        self.error = error
        self.calls = []

    def set_and_confirm(self, feature, new_state, index: int):
        self.calls.append((feature, new_state, index))

        if self.error is not None:
            raise self.error

        return self.confirmed_state


def make_state(*input_states: InputChannelState) -> dict:
    return {"input_channel": list(input_states)}


class US4x4CardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_input_icons_initialize_from_passed_state(self) -> None:
        card = US4x4Card(
            RecordingUS4x4Driver(),
            make_state(
                InputChannelState.ON,
                InputChannelState.OFF,
                InputChannelState.ON,
                InputChannelState.OFF,
            ),
        )

        try:
            self.assertTrue(card.input_icons[0].enabled_state)
            self.assertFalse(card.input_icons[1].enabled_state)
            self.assertTrue(card.input_icons[2].enabled_state)
            self.assertFalse(card.input_icons[3].enabled_state)
        finally:
            card.close()

    def test_input_click_writes_desired_state_and_uses_confirmed_state(self) -> None:
        driver = RecordingUS4x4Driver(confirmed_state=InputChannelState.OFF)
        card = US4x4Card(
            driver,
            make_state(
                InputChannelState.ON,
                InputChannelState.OFF,
                InputChannelState.OFF,
                InputChannelState.OFF,
            ),
        )

        try:
            card.input_icons[0].click()

            self.assertEqual(driver.calls, [(INPUT_CHANNEL, InputChannelState.OFF, 0)])
            self.assertFalse(card.input_icons[0].enabled_state)
        finally:
            card.close()

    def test_input_click_does_not_change_icon_when_driver_call_fails(self) -> None:
        driver = RecordingUS4x4Driver(error=RuntimeError("USB write failed"))
        card = US4x4Card(
            driver,
            make_state(
                InputChannelState.OFF,
                InputChannelState.OFF,
                InputChannelState.OFF,
                InputChannelState.OFF,
            ),
        )

        try:
            with patch("tuxam.ui.widgets.us4x4_card.QMessageBox.warning") as warning:
                card.input_icons[0].click()

            self.assertEqual(driver.calls, [(INPUT_CHANNEL, InputChannelState.ON, 0)])
            self.assertFalse(card.input_icons[0].enabled_state)
            warning.assert_called_once()
        finally:
            card.close()


if __name__ == "__main__":
    unittest.main()
