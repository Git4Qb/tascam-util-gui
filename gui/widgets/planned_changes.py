# gui/widgets/planned_changes.py

from dataclasses import dataclass, field


@dataclass
class PlannedChanges:
    header: str = "Changes you want to make:"
    order: list[str] = field(default_factory=list)
    lines: dict[str, str] = field(default_factory=dict)

    def set_line(self, key: str, text: str) -> None:
        self.lines[key] = text

    def remove(self, key: str) -> None:
        self.lines.pop(key, None)

    def clear(self) -> None:
        self.lines.clear()

    def render(self) -> str:
        out = [self.header]

        for key in self.order:
            if key in self.lines:
                out.append(self.lines[key])

        # Safety: include any unexpected keys at the end
        for key, text in self.lines.items():
            if key not in self.order:
                out.append(text)

        return "\n".join(out)
