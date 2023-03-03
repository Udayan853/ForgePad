from PySide6.QtWidgets import QApplication
from rootwindow import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow(app)

    window.show()
    app.exec()