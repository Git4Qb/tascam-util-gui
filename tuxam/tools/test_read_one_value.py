# tools/test_read_one_value.py

from __future__ import annotations

from tuxam.tools.domain.device_registry import US4X4
from tuxam.tools.transport.usb_transport import PyUsbTransport, CtrlRequest

# Prep sequence (interface-recipient, must target iface 4)
_PREP_BM = 0xA1
_PREP_B = 2
_PREP_WVALUE = 0x0100
_PREP_WINDEX = 0x2904  # IMPORTANT: low byte = interface number 4

# Vendor read/write
_READ_BM = 0xC0
_WRITE_BM = 0x40

COMMAND_POWERSAVE = 0x03
INDEX = 0

POWERSAVE_ON = 0x0100
POWERSAVE_OFF = 0x0000


def main() -> None:
    t = PyUsbTransport(US4X4.vendor_id, US4X4.product_id)

    try:
        t.open()
        print("Transport opened (iface 4 only)")

        def prep() -> None:
            t.ctrl_transfer_in(CtrlRequest(_PREP_BM, _PREP_B, _PREP_WVALUE, _PREP_WINDEX, 16))
            t.ctrl_transfer_in(CtrlRequest(_PREP_BM, _PREP_B, _PREP_WVALUE, _PREP_WINDEX, 50))

        # Read current
        prep()
        before = t.ctrl_transfer_in(CtrlRequest(_READ_BM, COMMAND_POWERSAVE, 0, INDEX, 1))
        print("before :", len(before), before.hex(" "))

        # Write ON (1)
        prep()
        w1 = t.ctrl_transfer_out(CtrlRequest(_WRITE_BM, COMMAND_POWERSAVE, 0, INDEX, data=bytes([1])))
        print("writeON:", w1)

        # Read back
        prep()
        after_on = t.ctrl_transfer_in(CtrlRequest(_READ_BM, COMMAND_POWERSAVE, 0, INDEX, 1))
        print("afterON:", len(after_on), after_on.hex(" "))

        # Write OFF (0) restore
        prep()
        w0 = t.ctrl_transfer_out(CtrlRequest(_WRITE_BM, COMMAND_POWERSAVE, 0, INDEX, data=bytes([0])))
        print("writeOFF:", w0)

        # Read back
        prep()
        after_off = t.ctrl_transfer_in(CtrlRequest(_READ_BM, COMMAND_POWERSAVE, 0, INDEX, 1))
        print("afterOFF:", len(after_off), after_off.hex(" "))

    finally:
        t.close()
        print("Transport closed")


if __name__ == "__main__":
    main()