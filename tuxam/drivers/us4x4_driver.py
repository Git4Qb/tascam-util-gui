# tuxam/drivers/us4x4_driver.py

from __future__ import annotations

from tuxam.drivers.base_driver import BaseDriver
from tuxam.devices.us_4x4 import parameters


class US4X4Driver(BaseDriver):
    parameters = parameters

    def read_device_state(self) -> dict:
        device_state = {}

        for name, feature in self.parameters.FEATURES.items():
            feature_state = []

            for index in feature:
                req = self._make_read_request(
                    b_request=feature.command_read,
                    w_value=0,
                    w_index=index,
                    length=1,
                )
                result = self.transport.ctrl_transfer_in(req)
                state = feature.possible_states(result[0])
                feature_state.append(state)

            device_state[name] = feature_state

        return device_state

    def write_feature_state(self, feature, new_state, index: int) -> None:
        req = self._make_write_request(
            b_request=feature.command_write,
            w_value=int(new_state),
            w_index=index,
            data=b"",
        )
        self.transport.ctrl_transfer_out(req)

    def read_feature_state(self, feature, index: int):
        req = self._make_read_request(
            b_request=feature.command_read,
            w_value=0,
            w_index=index,
            length=1,
        )
        result = self.transport.ctrl_transfer_in(req)
        return feature.possible_states(result[0])

    def set_and_confirm(self, feature, new_state, index: int):
        self.write_feature_state(feature, new_state, index)
        return self.read_feature_state(feature, index)