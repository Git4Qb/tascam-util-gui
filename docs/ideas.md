## Future idea: separate demo mode from real device mode

Timestamp: 2026-05-09 12:54 CEST

Goal:

Tuxam should support a separate demo mode for exploring supported device UIs without connected hardware.

Main principle:

Do not mix real USB devices and demo devices in the same device list. As more devices are supported, duplicated real/demo names would become confusing. Demo mode should be a separate app mode with its own device list.

Real mode:

- Scans connected Tascam USB devices
- Shows only detected real devices
- Opens real drivers/transports
- Sends changes to hardware immediately

Demo mode:

- Does not scan USB
- Shows a separate list of demo devices supported by the current app version
- Uses demo drivers/transports
- Lets users preview every supported device UI, not only connected hardware

Startup behavior:

- App starts in real mode
- App scans for connected Tascam devices automatically
- If devices are found, show normal device selection
- If no devices are found, show a dialog with:
  - Demo Mode
  - Rescan
  - Quit

Switching to demo mode:

User should be able to switch to demo mode from any point in the app.

If a real device is currently open, show a confirmation dialog:

```text
Changes made to your connected device have already been applied.
Demo mode will disconnect from the real device and open simulated devices instead.
Continue?
```

Buttons:

- Yes
- No

Switching back to real mode:

- User can switch from demo mode back to real devices
- App rescans USB devices
- If no devices are found, offer:
  - Rescan
  - Stay in Demo Mode
  - Quit

Implementation notes:

- Add explicit app mode state, for example `AppMode.REAL` and `AppMode.DEMO`
- Keep GUI separated from core logic
- Keep transport, device service, driver, and UI responsibilities separate
- Keep real and demo device management separate

Suggested structure:

- `RealDeviceService`
- `DemoDeviceService`
- `PyUsbTransport`
- `DemoTransport`

Current rough direction:

- Remove command-line `--demo` startup behavior
- Keep the idea of `DemoTransport`
- Build demo mode as a separate GUI mode

## Future idea: generate UI icon sizes automatically

Keep only the source/master icon in the repository:

`tuxam/ui/assets/icons/source/tuxam_icon.png`

During install/build, automatically generate required runtime icon sizes:

- 16x16
- 32x32
- 48x48
- 128x128
- 256x256

Generated files should go to:

`tuxam/ui/assets/icons/`

Possible script name:

`tools/generate_icons.sh`

Possible command:

```bash
for s in 16 32 48 128 256; do
  ffmpeg -y -i tuxam/ui/assets/icons/source/tuxam_icon.png \
    -vf scale=${s}:${s} \
    tuxam/ui/assets/icons/tuxam_icon_${s}.png
done
```
