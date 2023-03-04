from inspect import getsourcefile
import sys, os

if __name__ == "__main__":
    sys.path.append(os.path.dirname(getsourcefile(lambda:0)) + "/src")
    sys.path.append(os.path.dirname(getsourcefile(lambda:0)) + "/assets")

    from PySide6.QtWidgets import QApplication
    from rootwindow import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow(app)

    window.show()
    app.exec()