class TelegramStyle:
    COLORS = {
        "background": "#18222d",
        "primary": "#2b5278",
        "secondary": "#17212b",
        "text": "#ffffff",
        "text_secondary": "#8f98a0",
        "accent": "#5288c1",
        "button": "#2b5278",
        "button_hover": "#3d6d99",
        "button_pressed": "#1e3c5f",
        "success": "#5dc252",
        "error": "#eb5545",
        "warning": "#f0a732"
    }

    @classmethod
    def apply(cls, widget):
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: {cls.COLORS['background']};
                color: {cls.COLORS['text']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QPushButton {{
                background-color: {cls.COLORS['button']};
                color: {cls.COLORS['text']};
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: {cls.COLORS['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {cls.COLORS['button_pressed']};
            }}
            QLabel {{
                color: {cls.COLORS['text']};
            }}
            QTextEdit, QTextEdit:read-only {{
                background-color: {cls.COLORS['secondary']};
                border: 1px solid {cls.COLORS['primary']};
                border-radius: 4px;
                color: {cls.COLORS['text']};
                padding: 8px;
            }}
            QCheckBox {{
                color: {cls.COLORS['text']};
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {cls.COLORS['text_secondary']};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {cls.COLORS['accent']};
                border: 2px solid {cls.COLORS['accent']};
                border-radius: 3px;
            }}
            QGroupBox {{
                border: 1px solid {cls.COLORS['primary']};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                color: {cls.COLORS['text']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }}
            QScrollArea {{
                border: none;
            }}
            QScrollBar:vertical {{
                border: none;
                background: {cls.COLORS['secondary']};
                width: 8px;
                margin: 0 0 0 0;
            }}
            QScrollBar::handle:vertical {{
                background: {cls.COLORS['primary']};
                min-height: 20px;
                border-radius: 4px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: none;
            }}
            QStatusBar {{
                background-color: {cls.COLORS['secondary']};
                border-top: 1px solid {cls.COLORS['primary']};
            }}
            QProgressBar {{
                border: 1px solid {cls.COLORS['primary']};
                border-radius: 3px;
                text-align: center;
                background: {cls.COLORS['background']};
            }}
            QProgressBar::chunk {{
                background-color: {cls.COLORS['accent']};
                width: 10px;
            }}
        """)