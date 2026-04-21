# #!/usr/bin/env python3
# # tools/test_input_enable.py
# from faulthandler import is_enabled
# from tuxam.devices.device_registry import (
#     TASCAM_VENDOR_ID,
#     DEVICES_BY_PRODUCT_ID,
# )
# import usb.core
#
# VENDOR_ID = TASCAM_VENDOR_ID
# PRODUCT_ID = 0x804E
#
#
# def helper_transport_function():
#     dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
#     if dev is None:
#         raise SystemExit("Tascam device not found")
#
#     print("Tascam device found.")
#     return dev
#
#
# class DeviceInputs:
#     DEVICE = DEVICES_BY_PRODUCT_ID.get(PRODUCT_ID)
#
#     def __init__(self, device: DeviceID | None):
#         self.device = device
#
#
#
#     def get_input(self, number_of_inputs: int):
#
#         self.device = device
#         self.number_of_inputs = number_of_inputs
#
#         print("US-4x4 inputs: 1, 2, 3, 4")
#         valid_inputs = range(1, self.number_of_inputs + 1)
#         input_num = 0
#         is_enabled = bool
#         while True:
#             input_num = int(input("Select input to enable/disable (1-4): "))
#             print(f"Input no. {input_num} selected")
#             if input_num in valid_inputs:
#                 selected_input = input_num - 1
#
#             print("Select correct input number.")
#
# # input_state = bool(input(f'Enable input no. {input_num}?'))
# # if input_state == bool:
#
#
#     result = dev.ctrl_transfer(0x40, 6, is_enabled, selected_input)
#     print(f"Input {input_num} state has changed: {result}")
#     break
#
#     # can app detect number of inputs / outputs automatically?


import usb.core

VENDOR_ID = 0x0644
PRODUCT_ID = 0x804e

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
if dev is None:
    raise SystemExit("Tascam not found")

print("Device found.")

in_1 = 0
in_2 = 1
in_3 = 2
in_4 = 3

off = 0
on = 1


def input_enable(inp, state):
    inp = inp
    state = state
    result = dev.ctrl_transfer(0x040, 8, state, inp)

    print(f'Input {inp} is now set to {state}')
    return result

input_enable(in_1, on)
