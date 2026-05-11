# Tuxam Project Instructions

## Project Context

- Main application package is `tuxam/`
- PySide6 desktop application
- Keep GUI code separated from core logic
- Keep transport, device service, driver, and UI responsibilities separate

## Safety Rules

- Do not modify `.venv/`
- Do not install packages unless explicitly asked
- Do not push to GitHub
- Do not switch branches unless explicitly asked
- Do not merge branches automatically
- Explain intended edits before changing files

## Change Style

- Prefer minimal, focused changes
- Avoid unrelated cleanup during feature work
- Avoid mixing refactors with feature work
- Prefer simple, readable solutions over clever abstractions
- Prefer incremental refactors over large rewrites
- Warn before broad architectural changes or risky refactors

## Validation

- After edits, run:

  `.venv/bin/python -m compileall -q tuxam`

## Git Workflow

- Treat `redesign` as the stable development branch
- Treat `ui-experiments` as the branch for risky UI experiments
- Before larger UI changes, check the current branch and remind me if the work should stay on `ui-experiments`
- When an experimental change becomes stable and useful, suggest whether it should be merged or cherry-picked back into `redesign`
- Suggest a commit when a meaningful milestone is complete
- Keep commits focused and easy to understand
- Use Conventional Commit-style messages, for example:
  - `refactor(ui): redesign device selector and reorganize UI assets`
  - `chore(deps): update project requirements for redesign branch`

## Communication Preferences

- At the start of each Codex session, review `docs/ideas.md` to keep current project plans and active design direction in mind
- Briefly summarize what changed after each task
- Explain important architectural decisions briefly
- Point out when a pattern or workflow is good practice
- Warn when a solution may create technical debt
