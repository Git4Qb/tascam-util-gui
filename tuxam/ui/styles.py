# ui/styles.py

def vertical_gradient(top: str, bottom: str) -> str:
    return f"""
        background-color: qlineargradient(
            x1:0, y1:0, x2:0, y2:1,
            stop:0 {top},
            stop:1 {bottom}
        );
    """

COLORS = {
    "bg_main": "rgba(44, 44, 44, 200)",
    "paper": "#EFE3D3",
    "paper_border": "#C56A4C",
    "button_bg": "#d6d6d6",
    "button_bg_0": "#d6d6d6",
    "button_bg_0.5": "#bfbfbf",
    "button_bg_1": "#9e9e9e",
    "button_hover_0": "#FFFFFF",
    "button_hover_0.5": "#b0b0b0",
    "button_hover_1": "#333333",
    "button_disabled": "#777777",
    "text_dark": "#2C2C2C",
    "text_light": "#F5F5F5",
    "status_text": "#EFE3D3",
}

FONTS = {
    "main": "DejaVu Sans",
    "size_normal": 14,
    "size_status": 12,
    "size_penguin": 120,
    "size_device": 16,
}

SIZES = {
    "radius": 8,
    "padding": 8,
    "button_height": 36,
    "status_height": 24,
}


def get_main_window_style() -> str:
    return f"""
        QWidget {{
            background-color: transparent;
            font-family: "{FONTS["main"]}";
        }}
    """


def get_device_list_style(font_size: int = 14) -> str:
    return f"""
        QListWidget {{
            background: transparent;
            border: none;
            outline: none;
            color: {COLORS["text_dark"]};
            font-family: "{FONTS["main"]}";
            font-size: {font_size}px;
        }}

        QListWidget::viewport {{
            background: transparent;
        }}

        QListWidget::item {{
            background: transparent;
            border: none;
            padding: 4px 6px 4px 6px;
            margin-left: 6px;
            margin-right: 4px;
            color: {COLORS["text_dark"]};
        }}

        QListWidget::item:selected {{
            background: transparent;
            color: {COLORS["text_dark"]};
        }}

        QListWidget::item:hover {{
           background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS["button_hover_0"]},
                stop:0.5 {COLORS["button_hover_0.5"]},
                stop:1 {COLORS["button_hover_1"]}
            );
        }}
    """

def get_button_style() -> str:
    return f"""
        QPushButton {{
            background-color: {COLORS["button_bg_0"]};
            color: #2C2C2C;
            border: 1px solid #5a5a5a;
            border-radius: {SIZES["radius"]}px;
            padding: {SIZES["padding"]}px;
            min-height: {SIZES["button_height"]}px;
            font-family: "{FONTS["main"]}";
            font-size: {FONTS["size_normal"]}px;
        }}

        QPushButton:hover {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS["button_hover_0"]},
                stop:0.5 {COLORS["button_hover_0.5"]},
                stop:1 {COLORS["button_hover_1"]}
            );
        }}

        QPushButton:pressed {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {COLORS["button_hover_1"]},
                stop:0.5 {COLORS["button_hover_0.5"]},
                stop:1 {COLORS["button_hover_0"]}
            );
            padding-top: 10px;
            padding-bottom: 6px;
        }}

        QPushButton:disabled {{
            background-color: #3a3a3a;
            color: #888888;
            border: 1px solid #2a2a2a;
        }}
    """


def get_status_label_style() -> str:
    return f"""
        QLabel {{
            color: {COLORS["status_text"]};
            font-family: "{FONTS["main"]}";
            font-size: {FONTS["size_status"]}px;
            background: transparent;
        }}
    """


def get_device_label_style() -> str:
    return f"""
        QLabel {{
            color: {COLORS["text_light"]};
            font-family: "{FONTS["main"]}";
            font-size: {FONTS["size_device"]}px;
            font-weight: bold;
            background: transparent;
        }}
    """


def get_penguin_style() -> str:
    return f"""
        QLabel {{
            font-size: {FONTS["size_penguin"]}px;
            background: transparent;
        }}
    """


def get_panel_style() -> str:
    return f"""
        QFrame {{
            background-color: #111111;
            border-radius: 14px;
        }}
    """
