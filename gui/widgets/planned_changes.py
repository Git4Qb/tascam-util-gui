# gui/widgets/planned_changes.py
from dataclasses import dataclass, field

@dataclass
class PlannedChanges:
    header: str = "Changes you want to make:"
    order: list[str] = field(default_factory=list)

    # Display-only
    lines: dict[str, str] = field(default_factory=dict)

    # Apply-only (no string parsing)
    payloads: dict[str, dict] = field(default_factory=dict)

    def set(self, key: str, text: str, payload: dict) -> None:
        self.lines[key] = text
        self.payloads[key] = payload

    def remove(self, key: str) -> None:
        self.lines.pop(key, None)
        self.payloads.pop(key, None)

    def clear(self) -> None:
        self.lines.clear()
        self.payloads.clear()

    def render(self) -> str:
        out = [self.header]
        for key in self.order:
            if key in self.lines:
                out.append(self.lines[key])
        for key, text in self.lines.items():
            if key not in self.order:
                out.append(text)
        return "\n".join(out)