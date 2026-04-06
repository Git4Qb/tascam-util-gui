# tuxam/ui/styles.py

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
    "button_bg": "#7A8450",
    "button_hover": "#6c7647",
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


def get_paper_dropdown_style() -> str:
    return f"""
        QComboBox {{
            background: transparent;
            color: {COLORS["text_dark"]};
            border: none;
            padding: 8px 34px 8px 12px;
            font-family: "{FONTS["main"]}";
            font-size: {FONTS["size_normal"]}px;
            font-weight: 600;
        }}

        QComboBox:hover {{
            background: transparent;
            border: none;
        }}

        QComboBox:focus {{
            background: transparent;
            border: none;
            outline: none;
        }}

        QComboBox::drop-down {{
            border: none;
            width: 28px;
            background: transparent;
        }}

        QComboBox::down-arrow {{
            width: 12px;
            height: 12px;
            background: transparent;
        }}

        QComboBox QAbstractItemView {{
            background-color: rgba(239, 227, 211, 235);
            color: {COLORS["text_dark"]};
            border: 1px solid rgba(197, 106, 76, 120);
            padding: 4px;
            outline: 0;
        }}

        QComboBox QAbstractItemView::item {{
            padding: 8px 10px;
            background-color: transparent;
            color: {COLORS["text_dark"]};
            border: none;
        }}

        QComboBox QAbstractItemView::item:hover {{
            background-color: rgba(197, 106, 76, 120);
            color: {COLORS["text_light"]};
        }}
        
        QComboBox QAbstractItemView::item:selected {{
            background-color: rgba(239, 227, 211, 160);
            color: {COLORS["text_dark"]};
        }}
    """

def get_button_style() -> str:
    return f"""
        QPushButton {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #d6d6d6,
                stop:0.5 #bfbfbf,
                stop:1 #9e9e9e
            );
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
                stop:0 #FFFFFF
                stop:0.5 #b0b0b0
                stop:1 #333333
            );
        }}

        QPushButton:pressed {{
            background-color: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #9e9e9e,
                stop:0.5 #8a8a8a,
                stop:1 #6f6f6f
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


def get_background_frame_style() -> str:
    return """
            QFrame {
                background: transparent;
                border-radius: 0px;
            }
        """

def get_panel_style() -> str:
    return f"""
        QFrame {{
            background-color: #111111;
            border-radius: 14px;
        }}
    """