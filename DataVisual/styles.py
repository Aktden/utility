class TelegramStyle:
    COLORS = {
        "background": "#18222d",
        "primary": "#2b5278",
        "secondary": "#17212b",
        "text": "#ffffff",  # Белый цвет текста
        "text_secondary": "#8f98a0",
        "accent": "#5288c1",
        "button": "#2b5278",
        "button_hover": "#3d6d99",
        "button_pressed": "#1e3c5f",
        "success": "#5dc252",
        "error": "#eb5545",  # Красный цвет для ошибок (используем для галочек)
        "warning": "#f0a732"
    }
    @classmethod
    def apply(cls, widget):
        widget.setStyleSheet(f"""
            QWidget {{
                background-color: rgba(23, 33, 43, 0.7);  /* Полупрозрачный фон */
                color: {cls.COLORS['text']};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QMainWindow {{
                background: transparent;
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
                spacing: 10px;
                padding: 4px;
                font-size: 14px;    
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                background-color: {cls.COLORS['background']};
                border: 2px solid {cls.COLORS['text']};
                border-radius: 4px;
            }}
            QCheckBox::indicator:hover {{
                background-color: {cls.COLORS['primary']};
                border: 2px solid {cls.COLORS['button_hover']};
            }}
            QCheckBox::indicator:unchecked {{
                border: 2px solid {cls.COLORS['text']};  /* Белая рамка */
            }}
            QCheckBox::indicator:checked {{
                background-color: {cls.COLORS['error']};
            border: 2px solid {cls.COLORS['error']};
            }}
            QCheckBox::indicator:checked:hover {{
                background-color: #ff4444;
                border: 2px solid #ff5555;
                box-shadow: 0 0 8px #ff3333;
            }}
            /* Анимация переключения */
            QCheckBox::indicator {{
                 margin-right: 8px;
            }}
            /* Эффект при нажатии */
            QCheckBox::indicator:pressed {{
                background-color: {cls.COLORS['button_pressed']};
                border: 2px solid {cls.COLORS['accent']};
            }}
            /* Стиль для текста чекбокса при наведении */
            QCheckBox:hover {{
                color: {cls.COLORS['accent']};
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