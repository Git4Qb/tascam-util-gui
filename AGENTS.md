# Tuxam project instructions

- Main application package is `tuxam/`
- Do not modify `.venv/`
- Do not install packages unless asked
- Do not push to GitHub
- Prefer minimal changes
- Explain intended edits before changing files
- After edits run:
  .venv/bin/python -m compileall -q tuxam -x 'tuxam/tools/.*'
- Keep GUI separated from core logic
- PySide6 project
