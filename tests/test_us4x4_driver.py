from __future__ import annotations

import unittest

from tests.fakes import FakeTransport
from tuxam.devices.us_4x4.parameters import INPUT_CHANNEL, InputChannelState
from tuxam.drivers.us4x4_driver import US4X4Driver


class US4X4DriverTests(unittest.TestCase):
    def test_read_input_channel_returns_named_state(self) -> None:
        transport = FakeTransport()
        transport.open()
        transport.set_reply(
            bm=US4X4Driver.READ,
            b=INPUT_CHANNEL.command_read,
            v=0,
            i=0,
            length=1,
            data=bytes([InputChannelState.ON]),
        )

        driver = US4X4Driver(transport)
        state = driver.read_feature_state(INPUT_CHANNEL, 0)

        self.assertIs(state, InputChannelState.ON)
        self.assertEqual(len(transport.in_requests), 1)

        sent_request = transport.in_requests[0]
        self.assertEqual(sent_request.bm_request_type, US4X4Driver.READ)
        self.assertEqual(sent_request.b_request, INPUT_CHANNEL.command_read)
        self.assertEqual(sent_request.w_value, 0)
        self.assertEqual(sent_request.w_index, 0)
        self.assertEqual(sent_request.length, 1)

    def test_write_input_channel_records_request(self) -> None:
        transport = FakeTransport()
        transport.open()

        driver = US4X4Driver(transport)
        driver.write_feature_state(INPUT_CHANNEL, InputChannelState.ON, 0)

        self.assertEqual(len(transport.out_requests), 1)

        sent_request = transport.out_requests[0]
        self.assertEqual(sent_request.bm_request_type, US4X4Driver.WRITE)
        self.assertEqual(sent_request.b_request, INPUT_CHANNEL.command_write)
        self.assertEqual(sent_request.w_value, InputChannelState.ON)
        self.assertEqual(sent_request.w_index, 0)
        self.assertEqual(sent_request.data, b"")


if __name__ == "__main__":
    unittest.main()
