import sys
from PySide6.QtWidgets import QApplication
from window import VisualizerWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = VisualizerWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()