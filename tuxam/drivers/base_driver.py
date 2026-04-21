# tuxam/drivers/base_driver.py

from tuxam.transport.usb_transport import CtrlRequest, Transport


class BaseDriver:
    READ = 0xC0
    WRITE = 0x40

    def __init__(self, transport: Transport):
        self.transport = transport

    def _make_read_request(
        self,
        b_request: int,
        w_value: int,
        w_index: int,
        length: int,
    ) -> CtrlRequest:
        return CtrlRequest(
            bm_request_type=self.READ,
            b_request=b_request,
            w_value=w_value,
            w_index=w_index,
            length=length,
        )

    def _make_write_request(
        self,
        b_request: int,
        w_value: int,
        w_index: int,
        data: bytes,
    ) -> CtrlRequest:
        return CtrlRequest(
            bm_request_type=self.WRITE,
            b_request=b_request,
            w_value=w_value,
            w_index=w_index,
            data=data,
        )