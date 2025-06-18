from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QLabel
from PySide6.QtGui import QTextCharFormat, QColor
from PySide6.QtCore import Qt


class CheckBoxWithStatus(QWidget):
    def __init__(self, label_text):
        super().__init__()
        self.label_text = label_text
        self.checkbox = QCheckBox(label_text)
        self.status_label = QLabel("")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(2)

        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.checkbox, alignment=Qt.AlignLeft)
        layout.addLayout(checkbox_layout)

        self.status_label.setStyleSheet("font-size: 12px; color: #8f98a0;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def set_status(self, text, color="gray"):
        colors = {
            "gray": "#8f98a0",
            "green": "#5dc252",
            "red": "#eb5545",
            "blue": "#5288c1"
        }
        self.status_label.setText(text)
        self.status_label.setStyleSheet(f"color: {colors.get(color, color)}; font-size: 12px;")