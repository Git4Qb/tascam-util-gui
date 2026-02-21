# gui/profiles.py

def _profiles_path(self) -> Path:
    base = Path(__file__).resolve().parent
    d = base / self.PROFILE_DIRNAME
    d.mkdir(parents=True, exist_ok=True)
    return d / self.PROFILE_FILENAME


def _load_profiles(self) -> dict:
    path = self._profiles_path()
    if not path.exists():
        return {"devices": {}}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"devices": {}}


def _save_profiles(self, data: dict) -> None:
    self._profiles_path().write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _device_key(self) -> str:
    if self.device_manager is not None:
        desc = getattr(self.device_manager, "descriptor", None)
        if desc is not None:
            return f"{desc.vendor_id:04x}:{desc.product_id:04x}"
    return "offline"