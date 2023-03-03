from PySide6.QtWidgets import QMainWindow, QSpinBox, QFontComboBox, QFileDialog
from PySide6.QtCore import QFile, QTextStream, Qt
from PySide6.QtGui import QIcon, QFont, QActionGroup
from ui_mainwindow import Ui_MainWindow
import resources_rc

class MainWindow(QMainWindow):
    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.filename = ""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupActionGroup()
        self.setWindowTitle("GOATpad")
        self.setupStyle(":/Theme/theme/MaterialDark.qss")
        self.addWidgetsToToolbar()
        self.connectAllActions()
        self.setAppIcon()

    def setupActionGroup(self) -> None:
        self.ui.actGroup = QActionGroup(self)
        self.ui.actGroup.addAction(self.ui.actionLeftAlign)
        self.ui.actGroup.addAction(self.ui.actionCenterAlign)
        self.ui.actGroup.addAction(self.ui.actionRightAlign)
        self.ui.actGroup.addAction(self.ui.actionJustifyAlign)
        self.ui.actionLeftAlign.setChecked(True)

    def setAppIcon(self) -> None:
        self.app.setWindowIcon(QIcon("goat.png"))

    def connectAllActions(self) -> None:
        self.ui.actionOpen.triggered.connect(self.openFile)
        self.ui.actionSave.triggered.connect(self.saveFile)
        self.ui.actionSave_As.triggered.connect(self.saveAs)  
        self.ui.actionExit.triggered.connect(self.stopExecution)

        self.ui.actionCut.triggered.connect(self.ui.textEdit.cut)
        self.ui.actionCopy.triggered.connect(self.ui.textEdit.copy)
        self.ui.actionPaste.triggered.connect(self.ui.textEdit.paste)
        self.ui.actionUndo.triggered.connect(self.ui.textEdit.undo)
        self.ui.actionRedo.triggered.connect(self.ui.textEdit.redo)
        self.ui.actionClear.triggered.connect(self.ui.textEdit.clear)

        self.ui.actionBold.triggered.connect(self.boldText)
        self.ui.actionItalic.toggled.connect(self.ui.textEdit.setFontItalic)
        self.ui.actionUnderline.toggled.connect(self.ui.textEdit.setFontUnderline)
        self.ui.actionLeftAlign.triggered.connect(self.leftAlignText)
        self.ui.actionCenterAlign.triggered.connect(self.centerAlignText)
        self.ui.actionRightAlign.triggered.connect(self.rightAlignText)
        self.ui.actionJustifyAlign.triggered.connect(self.justifyAlignText)

        self.ui.fontStyle.currentFontChanged.connect(self.changeFont)
        self.ui.fontSize.valueChanged.connect(self.changeFontSize)

    def changeFontSize(self, data) -> None:
        self.ui.textEdit.setFontPointSize(data)

    def changeFont(self, data) -> None:
        self.ui.textEdit.setCurrentFont(data)
        
    def boldText(self, data) -> None:
        if data: self.ui.textEdit.setFontWeight(QFont.Bold) 
        else: self.ui.textEdit.setFontWeight(QFont.Normal)    

    def leftAlignText(self) -> None:
        self.ui.textEdit.setAlignment(Qt.AlignLeft)

    def rightAlignText(self) -> None:
        self.ui.textEdit.setAlignment(Qt.AlignRight)

    def centerAlignText(self) -> None:
        self.ui.textEdit.setAlignment(Qt.AlignCenter)
    
    def justifyAlignText(self) -> None:
        self.ui.textEdit.setAlignment(Qt.AlignJustify)

    def updateWindowName(self, name) -> None:
        self.setWindowTitle(f"GOATpad | {name}")

    def saveAs(self) -> None:
        self.filename = QFileDialog.getSaveFileName(self, "Save File")[0]
        print(self.filename)
        with open(self.filename, "w") as f:
            text = self.ui.textEdit.toPlainText()
            f.write(text)
        self.updateWindowName(self.filename.split("/")[-1])    

    def saveFile(self) -> None:
        if len(self.filename) > 0:
            with open(self.filename, "w") as f:
                text = self.ui.textEdit.toPlainText()
                f.write(text)
        else:
            self.saveAs()        

    def openFile(self) -> None:
        self.filename = QFileDialog.getOpenFileName(self, "Open file")[0]
        if(self.filename):
            with open(self.filename, "r") as f:
                self.ui.textEdit.insertPlainText(f.read())
            self.updateWindowName(self.filename.split("/")[-1])

    def stopExecution(self) -> None:
        self.app.quit()

    def addWidgetsToToolbar(self) -> None:
        self.ui.fontSize = QSpinBox()
        self.ui.fontSize.setValue(14)
        self.ui.fontStyle = QFontComboBox()
        self.ui.fontStyle.setCurrentFont("Times New Roman")
        self.ui.toolBar.insertWidget(self.ui.actionBold, self.ui.fontStyle)
        self.ui.toolBar.insertWidget(self.ui.actionBold, self.ui.fontSize)
        self.ui.toolBar.insertSeparator(self.ui.actionBold)

        self.ui.textEdit.setCurrentFont(QFont("Times New Roman", 14))

    def setupStyle(self, path) -> None:
        tmpFile = QFile(path)
        tmpFile.open(QFile.ReadOnly | QFile.Text)
        self.qss = QTextStream(tmpFile)
        self.app.setStyleSheet(self.qss.readAll()) 