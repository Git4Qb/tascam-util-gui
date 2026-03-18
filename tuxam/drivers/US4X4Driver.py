# tuxam/drivers/US4X4Driver.py

from __future__ import annotations
from tuxam.drivers.BaseDriver import BaseDriver
from tuxam.devices.us_4x4 import parameters


class US4X4Driver(BaseDriver):
    READ = 0xC0
    WRITE = 0x40
    parameters = parameters

    def read_4x4_state(self):
        device_state = {}

        for name, feature in self.parameters.FEATURES.items():
            feature_state = []

            for index in feature:
                result = self.dev.ctrl_transfer(
                    self.READ,
                    feature.command_read,
                    0,
                    index,
                    1,
                )
                state = feature.possible_states(result[0])
                feature_state.append(state)

            device_state[name] = feature_state

        return device_state


    def write_4x4_change(self, feature, new_state, index):
        self.dev.ctrl_transfer(
            self.WRITE,
            feature.command_write,
            int(new_state),
            index,
            None,
        )


    def read_feature_state(self, feature, index):
        result = self.dev.ctrl_transfer(
            self.READ,
            feature.command_read,
            0,
            index,
            1,
        )
        state = feature.possible_states(result[0])
        return state


    def set_and_confirm(self, feature, new_state, index):
        self.write_4x4_change(feature, new_state, index)
        return self.read_feature_state(feature, index)


    # def write_4x4_profile(self):
