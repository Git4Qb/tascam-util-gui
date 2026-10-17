# Project Status and Development Plans

## Scope

Tuxam is a PySide6 application for configuring supported Tascam USB audio
interfaces on Linux. The immediate development focus is completing US-4x4
support before adding another device. GUI redesign is deferred while the core
driver is being completed.

## Implemented

- Separate real-device and demo modes, with distinct device services.
- USB discovery with supported and unsupported device identification.
- Explicit device selection before opening a settings panel.
- In-memory US-4x4 demo transport.
- US-4x4 initial state reads for power saving, input enable, monitoring, and routing.
- Input-enable controls that write through the driver and display device readback.
- Transport cleanup when opening fails, the device panel closes, or the application
  closes.
- In-window handling of no-device and scan-error states.

Protocol definitions and simulated behavior do not establish hardware correctness.
Power saving, monitoring, and routing are modeled in the driver but do not yet
have GUI controls.

## US-4x4 Core Priorities

The next core milestone is request validation, after the pending repository
cleanup is complete. Invalid feature, index, and state arguments should be
rejected before USB access.

Subsequent work includes response validation, broader driver and transport test
coverage, and real-hardware verification of every modeled control. Hardware tests
should check write/readback behavior, actual audio behavior where applicable,
restoration of initial settings, and open/close behavior during audio streaming.

### Unresolved Protocol Detail

The routing write command is `0x10` in
`tuxam/devices/us_4x4/parameters.py`, but the command notes and routing tool use
decimal `10` (`0x0A`). Resolve this discrepancy against verified protocol evidence
before considering routing complete. Demo tests share the parameter definitions
and cannot independently confirm the command number.

## Architecture

- Keep USB transport, device discovery/services, device drivers, and GUI code
  separate.
- Keep device-specific protocol definitions in the corresponding device module.
- Display readback state after writes; do not assume the requested setting was
  accepted by the device.
- Keep real USB discovery out of demo mode.
- Prefer incremental changes over a general multi-device framework before a
  second device's requirements are understood.

## Deferred UI Work

Artwork normalization and launcher layout changes remain unfinished. If resumed:

- Use lowercase snake_case asset names and retain only necessary runtime assets.
- Normalize image canvas, scale, and alignment rather than accumulating runtime
  crop adjustments.
- Consider a shared launcher layout for no-device and device-selection states.
- Keep stable device/context information separate from transient operation status.
- Keep `MainWindow` focused on device lifecycle and view orchestration; extract
  shared views only where the existing code warrants it.
- Introduce device-card selection outside `MainWindow` when adding a second device.

These are proposals, not implemented features or prerequisites for core work.

## Later Work

- Packaging and user-facing installation/setup documentation.
- Additional device support after US-4x4 validation; evaluate existing Linux
  control interfaces before implementing another direct USB protocol.
- Consider generating runtime icon sizes from a single source during packaging.

## Validation

```bash
.venv/bin/python -m compileall -q tuxam
QT_QPA_PLATFORM=offscreen .venv/bin/python -m unittest discover -v
```

Automated tests cover simulated behavior. Real-device results should be recorded
separately with the device model, firmware when available, and tested operations.
