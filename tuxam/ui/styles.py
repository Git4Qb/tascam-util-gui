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
            font-weight: 600;
        }}

        QListWidget::viewport {{
            background: transparent;
        }}

        QListWidget::item {{
            background: transparent;
            border: none;
            padding: 4px 5px 4px 5px;
            margin-left: 3px;
            margin-right: 3px;
            color: {COLORS["text_dark"]};
        }}

        QListWidget::item:selected {{
            background: transparent;
            color: {COLORS["text_dark"]};
        }}

        QListWidget::item:hover {{
           background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 185),
                stop:0.45 rgba(255, 243, 222, 170),
                stop:1 rgba(221, 191, 152, 145)
            );
            border-radius: 5px;
            color: #4A2410;
        }}
    """

def get_button_style() -> str:
    return f"""
        QPushButton {{
            background-color: #1B1B1B;
            color: {COLORS["status_text"]};
            border: 1px solid #6D6256;
            border-radius: {SIZES["radius"]}px;
            padding: 8px 14px;
            min-height: {SIZES["button_height"]}px;
            font-family: "{FONTS["main"]}";
            font-size: {FONTS["size_normal"]}px;
        }}

        QPushButton:hover {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #37312B,
                stop:1 #211D1A
            );
            border-color: #B09A83;
            color: #FFF7EE;
        }}

        QPushButton:pressed {{
            background-color: #151210;
            border-color: #7B6B5B;
            color: #E8DCCF;
        }}

        QPushButton:disabled {{
            background-color: #202020;
            color: #686868;
            border: 1px solid #303030;
        }}
    """


def get_primary_button_style() -> str:
    return f"""
        QPushButton {{
            background-color: #E8E1D6;
            color: #1F1F1F;
            border: 1px solid #F3EFE8;
            border-radius: {SIZES["radius"]}px;
            padding: 8px 16px;
            min-height: {SIZES["button_height"]}px;
            font-family: "{FONTS["main"]}";
            font-size: {FONTS["size_normal"]}px;
            font-weight: 600;
        }}

        QPushButton:hover {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFFFFF,
                stop:0.45 #FFF3DE,
                stop:1 #DDBF98
            );
            border: 1px solid #FFD18B;
            color: #080808;
        }}

        QPushButton:pressed {{
            background-color: #B99D7A;
            border-color: #D7B276;
            color: #171717;
        }}

        QPushButton:disabled {{
            background-color: #202020;
            color: #686868;
            border: 1px solid #303030;
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


def get_empty_state_title_style() -> str:
    return f"""
        QLabel {{
            color: {COLORS["status_text"]};
            font-family: "{FONTS["main"]}";
            font-size: 20px;
            font-weight: bold;
            background: transparent;
        }}
    """


def get_empty_state_detail_style() -> str:
    return f"""
        QLabel {{
            color: {COLORS["status_text"]};
            font-family: "{FONTS["main"]}";
            font-size: {FONTS["size_normal"]}px;
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
