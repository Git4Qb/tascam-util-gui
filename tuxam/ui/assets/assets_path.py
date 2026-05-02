# ui/assets/assets_path.py

from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

def asset(name: str) -> Path:
    return ASSETS_DIR / name

def icon(name: str) -> str:
    return str(ASSETS_DIR / "icons" / name)