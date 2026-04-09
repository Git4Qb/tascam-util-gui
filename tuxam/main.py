# main.py

from tuxam.devices.device_manager import select_driver
import usb.core

def main():

    driver = select_driver()

    if not driver:
        print("No supported Tascam device found.")
        return

    print("Driver selected:", type(driver).__name__)
    try:
        state = driver.read_4x4_state()
        print("Device state:", state)
    except usb.core.USBError as e:
        print("USBError:", e)

if __name__ == "__main__":
    main()