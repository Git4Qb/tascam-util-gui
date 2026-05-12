"""User-facing UI text."""

BUTTON_DEMO_MODE = "Demo mode"
BUTTON_DEMO_MODE_CTA = "Demo Mode"
BUTTON_OPEN_DEVICE = "Open device"
BUTTON_QUIT = "Quit"
BUTTON_REAL_DEVICES = "Real devices"
BUTTON_RESCAN = "Rescan"
BUTTON_TRY_AGAIN = "Try Again"

DEMO_NOTICE = "Demo Mode - simulated device, no hardware changes"

DIALOG_SWITCH_TO_DEMO_TITLE = "Switch to Demo Mode"
DIALOG_SWITCH_TO_DEMO_TEXT = (
    "Changes made to your connected device have already been applied.\n"
    "Demo mode will disconnect from the real device and open simulated devices instead.\n"
    "Continue?"
)

EMPTY_NO_REAL_DEVICES_TITLE = "No Tascam device found"
EMPTY_NO_REAL_DEVICES_DETAIL = (
    "Connect a Tascam USB interface and rescan, or open Demo Mode."
)
EMPTY_NO_DEMO_DEVICES_TITLE = "No demo devices available"
EMPTY_NO_DEMO_DEVICES_DETAIL = (
    "This app version does not provide any simulated devices."
)
EMPTY_SCAN_ERROR_TITLE = "Device scan failed"

STATUS_CLOSE_PANEL_FIRST = "Close device panel before opening another device"
STATUS_DEMO_ENABLED = "Demo mode enabled"
STATUS_DEVICE_NOT_OPENED = "Device not opened"
STATUS_DEVICE_PANEL_ALREADY_OPEN = "Device panel is already open"
STATUS_DEVICE_PANEL_CLOSED = "Device panel closed"
STATUS_NO_DEMO_DEVICES = "No demo devices available"
STATUS_NO_TASCAM_DEVICES = "No Tascam devices found"
STATUS_REAL_MODE_ENABLED = "Real device mode enabled"
STATUS_SELECT_DEVICE = "Select a device and click Open device"
STATUS_SELECT_SUPPORTED_DEVICE = "Select a supported device first"
STATUS_SIMULATED_DEVICE_SELECTED = "Simulated device selected"
STATUS_SUPPORTED_DEVICE_SELECTED = "Supported device selected"
STATUS_UNSUPPORTED_DEVICE = "This device is not supported yet"


def scan_error_detail(error: object) -> str:
    return f"Could not scan USB devices: {error}"


def scan_error_status(error: object) -> str:
    return f"Device scan failed: {error}"


def open_failed_status(error: object) -> str:
    return f"Open failed: {error}"


def device_opened_status(label: str) -> str:
    return f"{label} opened"
