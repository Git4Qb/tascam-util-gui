## Work snapshot: 2026-05-13 21:04 CEST

Planned commit:

- `fix(ui): wire input controls to confirmed driver state`

Current development context:

- Active branch is `ui-experiments`
- Local branch is ahead of `origin/ui-experiments` by 1 commit before this milestone is committed
- This work is still experimental UI/device-panel cleanup and should stay on `ui-experiments`
- `redesign` remains the stable development branch for useful UI work after it settles

Done in this stage:

- Fixed `MainWindow` open-failure cleanup so a partially opened driver transport is closed if reading initial device state or creating the card fails
- Added regression coverage for open failure after a driver has already been returned by the device service
- Wired US-4x4 input channel icons to the driver instead of toggling only local GUI state
- Initialized US-4x4 input icons from the fresh state snapshot read when the device panel opens
- Changed input clicks to call `set_and_confirm()` and update icons from the confirmed readback state
- Kept the input icon unchanged and showed a warning if a driver write/readback fails
- Added US-4x4 card tests for initial state, driver writes, confirmed readback, and failure handling
- Kept `set_and_confirm()` because it is the useful write-then-readback operation; only its name may need clarification later

Current state:

- Opening a device now has safer cleanup around transport ownership
- The first real US-4x4 control path is connected end-to-end: initial device state -> UI state -> driver write -> confirmed UI state
- `MainWindow` still owns orchestration for opening a selected device and reading initial state
- `US4x4Card` now owns input-channel interaction for an already-open driver
- `MainWindow` remains the next maintenance pressure point after this functional fix

Validation:

- `.venv/bin/python -m compileall -q tuxam`
- `.venv/bin/python -m unittest discover -v`

Next reasonable steps:

- Commit this functional milestone before visual or structural follow-up work
- If desired, update the no-device penguin artwork as a separate UI polish commit
- Extract a `DeviceSelectorView` to own `PenguinSelector`, device actions, selection clearing, and selector signals
- Keep `MainWindow` focused on orchestration: scan, mode switch, open device, and view routing
- Add a simple device-card factory or registry before adding a second supported device so `MainWindow` no longer hard-codes `US4x4Card`
- Replace the direct `demo_notice_label` in `MainWindow` with a cleaned-up reusable `ModeBadge`, or remove `mode_badge.py` if the badge abstraction is not useful
- Rename `set_and_confirm()` later if the current name stays confusing, for example to `write_and_read_feature_state()`

## Work snapshot: 2026-05-12 18:33 CEST

Latest commit:

- `035fbe3 refactor(ui): clarify demo mode indicator and device selection`

Current development context:

- Active branch is `ui-experiments`
- Local branch is ahead of `origin/ui-experiments` by 1 commit
- Current work is still experimental UI cleanup and should stay on `ui-experiments`
- `redesign` remains the stable development branch for useful UI work after it settles

Done in this stage:

- Added a persistent demo-mode notice so simulated devices are always visible
- Kept real mode visually normal and hid the demo notice outside demo mode
- Prevented device scan/startup from auto-selecting the first device
- Fixed device selection so mouse and keyboard selection use the same row-change path
- Blocked list selection signals while scan results are rebuilt
- Added `tuxam/ui/messages.py` for shared user-facing UI text
- Moved main-window and no-device view status/button text to the shared messages module
- Improved selected-row styling in the device selector
- Added demo-mode UI tests for startup scan, selection, and opening a selected demo device

Current state:

- Demo mode is clearer without changing the whole app theme
- A user must explicitly select a device before `Open device` is enabled
- Device list selection state is less fragile after rescans
- User-facing text is no longer scattered only through `main_window.py`
- `main_window.py` is still too large and remains the next maintenance pressure point

Validation:

- `.venv/bin/python -m compileall -q tuxam`
- `.venv/bin/python -m unittest discover -v`

Next reasonable steps:

- Replace the direct `demo_notice_label` in `MainWindow` with a cleaned-up reusable `ModeBadge`, or remove `mode_badge.py` if the badge abstraction is not useful
- Extract a `DeviceSelectorView` to own `PenguinSelector`, device actions, selection clearing, and selector signals
- Keep `MainWindow` focused on orchestration: scan, mode switch, open device, and view routing
- Add a simple device-card factory or registry so `MainWindow` no longer hard-codes `US4x4Card`
- Wire `US4x4Card` controls to initial driver state and real driver writes
- After those pieces are stable, decide whether to cherry-pick or merge the useful UI work back to `redesign`

## Work snapshot: 2026-05-12 00:31 CEST

Latest commit:

- `8a77134 refactor(ui): simplify no-device flow and polish selector controls`

Done in this stage:

- Replaced the startup no-device popup with an in-window `NoDeviceView`
- Removed the upper action row and moved actions into contextual center-view controls
- Added `penguin_no_device.png` for the no-device empty state
- Restyled primary and secondary buttons with lighter, warmer hover/pressed states
- Improved device-list readability, hover styling, and label fit on the selector flipboard
- Shortened displayed Tascam device names in selector lists, for example `US-4X4 (Demo)`
- Added a separate scan-error UI state with `Try Again`, `Demo Mode`, and `Quit`
- Added test coverage for the scan-error UI state
- Updated validation instructions to compile all of `tuxam`

Current state:

- The app has a cleaner launcher-style main window
- No-device, scan-error, and device-selector states are visually separated
- Real/demo device list separation remains intact
- The branch is a good experimental UI milestone on `ui-experiments`

Next reasonable steps:

- Add a persistent but subtle `Demo Mode` indicator so simulated devices are always obvious
- Decide where the demo indicator belongs now that the upper action row is gone
- Consider demo-mode status text such as `Simulated device selected`
- Keep real mode visually normal and avoid a full theme swap
- After the demo indicator is stable, consider whether this UI work should be cherry-picked or merged back to `redesign`
- Later, if `main_window.py` keeps growing, extract a `DeviceSelectorView` instead of doing a broad architecture rewrite

## Future idea: separate demo mode from real device mode

Timestamp: 2026-05-09 12:54 CEST

Status update: 2026-05-10

Implemented in `feat(ui): add explicit demo mode switching`:

- App starts in real mode with explicit `AppMode.REAL`
- Demo mode is represented by explicit `AppMode.DEMO`
- Command-line `--demo` startup behavior has been removed
- Real and demo device lists are selected through separate services
- `DemoDeviceService` and `DemoTransport` provide an in-memory US-4x4 demo device
- Startup with no real devices offers Demo Mode, Rescan, and Quit
- Demo mode can switch back to real device mode
- If no real devices are found after switching back, the app offers Rescan, Stay in Demo Mode, and Quit

Next UI direction:

- Keep startup no-device handling inside the main window instead of showing a separate popup
- Keep actions contextual to the current center view:
  - No-device view: Rescan, Demo Mode, Quit
  - Device selector view: Open device, Rescan, mode switch
- Keep the upper action row removed so the center view has more room
- Make demo mode visually persistent so users always know whether they are using real hardware or simulated devices
- Start with a small persistent `Demo Mode` badge near the selector/actions area, possibly reusing `ModeBadge`
- Consider changing status text in demo mode to mention simulated devices
- Keep real mode visually normal
- Avoid redesigning the device settings card until the basic mode indicator is clear

Follow-up review notes:

- Rescan now closes an open device panel before scanning, avoiding a stale driver reference in a separate panel.
- The startup no-device popup has been removed; the no-device state is now handled by `NoDeviceView`.
- Device scan errors should become their own UI state instead of being represented by the generic no-device empty state.

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
- If no devices are found, show the in-window no-device view with:
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
- If no devices are found, show the in-window no-device view with:
  - Rescan
  - Demo Mode
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
