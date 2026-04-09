# drivers/base_driver.py

class BaseDriver:
    READ = 0xC0
    WRITE = 0x40

    def __init__(self, usb_device):
        self.dev = usb_device
