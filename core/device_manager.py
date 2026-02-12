# core/device_manager.py

from core.protocol import VENDOR_ID, PRODUCT_ID
from core.transport import PyUsbTransport, DeviceNotFound, PermissionDenied, TransportError

def connect(self) -> bool:
    self._transport = PyUsbTransport(VENDOR_ID, PRODUCT_ID)
    try:
        self._transport.open()
        self.connected = True
        return True
    except (DeviceNotFound, PermissionDenied, TransportError):
        self._transport = None
        self.connected = False
        return False
