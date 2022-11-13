# https://stackoverflow.com/questions/15263063/why-keypress-event-in-pyqt-does-not-work-for-key-enter
# STOP button - https://stackoverflow.com/questions/27802270/how-to-stop-a-function

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTableWidget, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
import matplotlib
from os import listdir
import re  # maybe need to use for data validation/verification
from mainExecution import main_execute

# Access main window from child - https://stackoverflow.com/questions/72169262/pyqt5-access-mainwindow-from-another-window

# TO BE IMPLEMENTED/LOOKED INTO:
# - If parent window shuts, so does any child window
# - QVBoxLayout() - Reactive design?


class SaveWindow(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(550, 370, 350, 130)  # Size of the window
        name = QtWidgets.QLabel(self)
        name.setText("<b>Save script</b>")
        font = name.font()
        font.setPointSize(20)
        name.setFont(font)
        name.move(115, 10)

        self.name = QtWidgets.QTextEdit(self)
        self.name.move(100, 40)
        self.name.resize(140, 30)

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.switch)
        b1.move(125, 70)

    def switch(self):
        self.switch_window.emit(self.name.toPlainText() + ".txt")


class LoadWindow(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(550, 370, 350, 130)  # Size of the window
        name = QtWidgets.QLabel(self)
        name.setText("<b>Load script</b>")
        font = name.font()
        font.setPointSize(20)
        name.setFont(font)
        name.move(115, 10)

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.move(100, 40)
        self.comboBox.resize(140, 30)

        onlyfiles = [f for f in listdir("./ui/scripts/")]
        txtFiles = [f for f in onlyfiles if re.search("\.txt", f) != None]
        self.comboBox.addItems(txtFiles)

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.select)
        b1.move(125, 70)

    def select(self):
        # Use ReGex to employ data validation/verification
        # If self.input1 is not empty ect
        self.switch_window.emit(self.comboBox.currentText())


class VariableWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(550, 370, 350, 170)  # Size of the window
        name = QtWidgets.QLabel(self)
        name.setText("<b>Variable assignment</b>")
        font = name.font()
        font.setPointSize(20)
        name.setFont(font)
        name.move(85, 10)

        name2 = QtWidgets.QLabel(self)
        name2.setText("Variable name: ")
        font2 = name2.font()
        font2.setPointSize(15)
        name2.setFont(font2)
        name2.move(10, 47)
        self.input1 = QtWidgets.QLineEdit(self)
        self.input1.move(125, 45)
        self.input1.resize(210, 30)
        self.input1.installEventFilter(self)  # Allows event detection

        name3 = QtWidgets.QLabel(self)
        name3.setText("Value:")
        font3 = name3.font()
        font3.setPointSize(15)
        name3.setFont(font3)
        name3.move(10, 87)
        self.input2 = QtWidgets.QLineEdit(self)
        self.input2.resize(210, 30)
        self.input2.move(125, 85)
        self.input2.installEventFilter(self)  # Allows event detection

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.switch)
        b1.move(120, 125)

    def switch(self):
        self.switch_window.emit(self.input1.text() + "=" + self.input2.text())


class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()
    switch_window2 = QtCore.pyqtSignal()
    switch_window3 = QtCore.pyqtSignal()

    def __init__(self, text, outputText, scriptText, pos, var, save, load):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(100, 100, 1250, 700)
        self.setWindowTitle('MathChamp')

        # Name at the top of application
        name = QtWidgets.QLabel(self)
        name.setText("<b>MathChamp</b>")
        font = name.font()
        font.setPointSize(40)
        name.setFont(font)
        name.resize(235, 60)
        name.move(90, 0)

        # Label at the top of application
        label = QLabel(self)
        pixmap = QPixmap('./ui/templogo.jpg')
        label.setPixmap(pixmap.scaled(55, 55))
        label.adjustSize()
        label.move(26, 7)

        # Scripting box
        self.scriptBox = QtWidgets.QTextEdit(self)
        self.scriptBox.resize(851, 448)
        self.scriptBox.move(25, 70)
        self.scriptBox.setAlignment(Qt.AlignTop)  # Alignment of text
        self.scriptBox.installEventFilter(self)  # Allows event detection
        cursor = QtGui.QTextCursor(self.scriptBox.document())
        cursor.beginEditBlock()
        cursor.insertText(scriptText)
        cursor.endEditBlock()

        # Output
        self.outputBox = QtWidgets.QTextEdit(self)
        self.outputBox.resize(990, 146)
        self.outputBox.move(25, 527)
        self.outputBox.setAlignment(Qt.AlignTop)  # Alignment of text
        self.outputBox.installEventFilter(self)  # Allows event detection

        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        #cursor.insertText(">> ") TEMPORARY

        if var != None:  # variable window text
            cursor.insertText(text)

        if save != None:
            with open('./ui/scripts/' + text, 'w') as f:  # Need to fix
                f.write(self.scriptBox.toPlainText())

            self.outputBox.setText(outputText)

        if load != None:
            with open('./ui/scripts/' + text, 'r') as f:
                self.scriptBox.setText(f.read())

            self.outputBox.setText(outputText)

        if (self.outputBox.toPlainText() + text) == ">> ":
            cursor.insertText(text)

        self.firstPos = cursor.position()

        if self.firstPos != 3:
            self.firstPos = pos

        cursor.endEditBlock()

        self.savedHtmlText = self.outputBox.toHtml()
        self.savedPlainText = self.outputBox.toPlainText()

        # Variable table
        table = QtWidgets.QTableWidget(self)
        table.setRowCount(100)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Variable name", "Value"])
        table.setColumnWidth(0, 153)  # indexing table at 0
        table.setColumnWidth(1, 153)
        table.resize(337, 447)
        table.move(887, 70)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)  # user can't edit variable table

        # Buttons
        self.runButton = QtWidgets.QPushButton(self)
        self.runButton.setText("RUN")
        self.runButton.setIcon(QIcon('./ui/start.jpg'))
        self.runButton.clicked.connect(self.run_script)  # runs text in script window
        self.runButton.resize(70, 75)
        self.runButton.move(1020, 522)

        self.stopButton = QtWidgets.QPushButton(self)
        self.stopButton.setText("STOP")
        self.stopButton.setIcon(QIcon('./ui/stop.jpg'))
        # self.stopButton.clicked.connect(clicked)  # connected to a function
        self.stopButton.resize(70, 75)
        self.stopButton.move(1089, 522)

        self.plotButton = QtWidgets.QPushButton(self)
        self.plotButton.setText("PLOT")
        # self.plotButton.clicked.connect(clicked)  # connected to a function
        self.plotButton.resize(70, 75)
        self.plotButton.move(1159, 522)

        self.varButton = QtWidgets.QPushButton(self)
        self.varButton.setText("Create variable")
        self.varButton.clicked.connect(self.variable)
        self.varButton.resize(210, 31)
        self.varButton.move(1020, 592)

        self.sinButton = QtWidgets.QPushButton(self)
        self.sinButton.setText("sin")
        self.sinButton.clicked.connect(self.sin)  # connected to a function
        self.sinButton.resize(50, 31)
        self.sinButton.move(1020, 619)

        self.cosButton = QtWidgets.QPushButton(self)
        self.cosButton.setText("cos")
        self.cosButton.clicked.connect(self.cos)  # connected to a function
        self.cosButton.resize(50, 31)
        self.cosButton.move(1060, 619)

        self.tanButton = QtWidgets.QPushButton(self)
        self.tanButton.setText("tan")
        self.tanButton.clicked.connect(self.tan)  # connected to a function
        self.tanButton.resize(50, 31)
        self.tanButton.move(1100, 619)

        self.sqrtButton = QtWidgets.QPushButton(self)
        self.sqrtButton.setText("sqrt")
        self.sqrtButton.clicked.connect(self.sqrt)  # connected to a function
        self.sqrtButton.resize(50, 31)
        self.sqrtButton.move(1140, 619)

        self.lnButton = QtWidgets.QPushButton(self)
        self.lnButton.setText("ln")
        self.lnButton.clicked.connect(self.ln)  # connected to a function
        self.lnButton.resize(50, 31)
        self.lnButton.move(1180, 619)

        self.logxButton = QtWidgets.QPushButton(self)
        self.logxButton.setText("logx")
        self.logxButton.clicked.connect(self.logx)  # connected to a function
        self.logxButton.resize(50, 31)
        self.logxButton.move(1020, 646)

        self.log10Button = QtWidgets.QPushButton(self)
        self.log10Button.setText("log10")
        self.log10Button.clicked.connect(self.log10)  # connected to a function
        self.log10Button.resize(50, 31)
        self.log10Button.move(1060, 646)

        self.fxButton = QtWidgets.QPushButton(self)
        self.fxButton.setText("f(x)")
        self.fxButton.clicked.connect(self.fx)  # connected to a function
        self.fxButton.resize(50, 31)
        self.fxButton.move(1100, 646)

        self.piButton = QtWidgets.QPushButton(self)
        self.piButton.setText("π")
        self.piButton.clicked.connect(self.pi)  # connected to a function
        self.piButton.resize(50, 31)
        self.piButton.move(1140, 646)

        self.expButton = QtWidgets.QPushButton(self)
        self.expButton.setText("e")
        self.expButton.clicked.connect(self.exponent)  # connected to a function
        self.expButton.resize(50, 31)
        self.expButton.move(1180, 646)

        self.loadButton = QtWidgets.QPushButton(self)
        self.loadButton.setText("Load")
        self.loadButton.clicked.connect(self.load)  # connected to a function
        self.loadButton.resize(60, 31)
        self.loadButton.move(820, 40)

        self.saveButton = QtWidgets.QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.save)  # connected to a function
        self.saveButton.resize(60, 31)
        self.saveButton.move(770, 40)

    def sin(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("sin()")
        cursor.endEditBlock()

    def cos(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("cos()")
        cursor.endEditBlock()

    def tan(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("tan()")
        cursor.endEditBlock()

    def sqrt(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("sqrt()")
        cursor.endEditBlock()

    def ln(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("ln()")
        cursor.endEditBlock()

    def logx(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("logx()")
        cursor.endEditBlock()

    def log10(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("log10()")
        cursor.endEditBlock()

    def fx(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("fx()")
        cursor.endEditBlock()

    def pi(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("3.141592653589793238")
        cursor.endEditBlock()

    def exponent(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("exponent()")
        cursor.endEditBlock()

    def run_script(self):  # For running the main input script
        cursor = self.scriptBox.textCursor()  # Cursor of the input box
        cursor2 = QtGui.QTextCursor(self.outputBox.document())  # Cursor of the output box

        if cursor.hasSelection():  # If text is highlighted
            # Output highlighted text on the command line
            selected = self.scriptBox.toPlainText()[cursor.selectionStart():cursor.selectionEnd()].strip()
            script_type = "Running partial script...\n"

        else:
            selected = self.scriptBox.toPlainText().strip()  # Output whole script on command line
            script_type = "Running script...\n"

        cursor2.beginEditBlock()
        cursor2.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        cursor2.insertText(script_type)  # Output that the whole script is running

        for line in selected.splitlines():
            cursor2.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)  # moves cursor to end
            cursor2.insertText(">> " + line + "\n")
            try:
                cursor2.insertText(str(main_execute(line)) + "\n")
            except:
                cursor2.insertText("ERROR: Issue at line " + str(selected.splitlines().index(line)+1) + "\n")
                break

        cursor2.insertText(">> ")
        self.firstPos = cursor2.position()  # records first position of cursor line (for string output)
        cursor2.endEditBlock()

        self.savedPlainText = self.outputBox.toPlainText()  # Save the plain text
        self.savedHtmlText = self.outputBox.toHtml()  # Save the HTML (i.e. if text bolded, coloured etc)

    def variable(self):
        self.switch_window.emit()

    def save(self):
        self.switch_window2.emit()

    def load(self):
        self.switch_window3.emit()

    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.KeyPress and obj is self.outputBox:

            if event.key() == QtCore.Qt.Key_Backspace and self.outputBox.hasFocus():

                if self.savedPlainText.strip() == self.outputBox.toPlainText().strip():
                    cursor = QtGui.QTextCursor(self.outputBox.document())
                    cursor.beginEditBlock()
                    cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
                    cursor.insertText("\n>> ")
                    cursor.endEditBlock()

                    self.outputBox.setText(self.savedHtmlText)
                    self.outputBox.moveCursor(QtGui.QTextCursor.End)

            if event.key() == QtCore.Qt.Key_Return and self.outputBox.hasFocus():
                # Testing - not finished - Key press enter event handling

                # Need a way to see the line that was returned? So we can lex and parse?

                self.savedHtmlText = self.outputBox.toHtml()

                cursor = QtGui.QTextCursor(self.outputBox.document())
                cursor.beginEditBlock()
                cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
                self.lastPos = cursor.position()

                # ReGeX here - Implement this? Or maybe implement cursor.position() better? Look into this...
                # Not super amused with implementation here...
                line = self.outputBox.toPlainText()[self.firstPos: self.lastPos].replace('>>','').strip()

                if line=='clear':
                    self.outputBox.setText("")
                    cursor.insertText(">> ")
                    self.firstPos = cursor.position()
                    print("Output box to be cleared - DONE")
                    print("Variables need to be cleared")
                    print("Clear previous line count [^]")
                    print("This implementation is not finished")
                    cursor.endEditBlock()
                else:
                    print("Line output: " + line)

                    try:
                        cursor.insertText("\n"+str(main_execute(line)))
                    except:
                        cursor.insertText("\nException!")

                    #self.firstPos = self.lastPos
                    self.firstPos = cursor.position()
                    cursor.insertText("\n>> ")
                    cursor.endEditBlock()

                self.savedHtmlText = self.outputBox.toHtml()
                self.savedPlainText = self.outputBox.toPlainText()

        return super().eventFilter(obj, event)


class Controller:

    outputBoxText = ">> "
    inputBoxText = ""
    pos = 0

    def __init__(self):
        pass

    def show_main(self, text=">> "):

        # Closing sub-windows if they're open
        try:
            self.window.close()
        except:
            self.window=None

        try:
            self.saveWin.close()
        except:
            self.saveWin=None

        try:
            self.loadWin.close()
        except:
            self.loadWin=None

        if self.window != None:
            self.outputBoxText = self.main.savedPlainText
            text = self.outputBoxText + text

        self.main = MainWindow(text, self.outputBoxText, self.inputBoxText, self.pos, self.window, self.saveWin, self.loadWin)
        self.window = None
        self.saveWin = None
        self.loadWin = None

        # These lines here causing issue??

        self.main.switch_window.connect(self.show_var)
        self.main.switch_window2.connect(self.show_save)
        self.main.switch_window3.connect(self.show_load)

        self.main.show()

    def show_var(self):
        self.window = VariableWindow()

        self.outputBoxText = self.main.savedPlainText
        self.inputBoxText = self.main.scriptBox.toPlainText()
        self.pos = self.main.firstPos

        self.window.switch_window.connect(self.show_main)
        self.window.show()

    def show_save(self):
        self.saveWin = SaveWindow()

        self.outputBoxText = self.main.savedPlainText
        self.inputBoxText = self.main.scriptBox.toPlainText()
        self.pos = self.main.firstPos

        self.saveWin.switch_window.connect(self.show_main)
        self.saveWin.show()

    def show_load(self):
        self.loadWin = LoadWindow()

        self.outputBoxText = self.main.savedPlainText
        self.inputBoxText = self.main.scriptBox.toPlainText()
        self.pos = self.main.firstPos

        self.loadWin.switch_window.connect(self.show_main)
        self.loadWin.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()