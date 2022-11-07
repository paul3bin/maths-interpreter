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
from os.path import isfile, join
import re  # maybe need to use for data validation/verification

# Access main window from child - https://stackoverflow.com/questions/72169262/pyqt5-access-mainwindow-from-another-window

# TO BE IMPLEMENTED/LOOKED INTO:
# - If parent window shuts, so does any child window
# - QVBoxLayout() - Reactive design?

def clicked():  # testing method - will be deleted as development progresses (TEMPORARY)
    print("clicked")

# Class for the main window of 'MathChamp' application
class MainWindow(QWidget):

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

    def save(self):  # throws error
        with open('./ui/scripts/script.txt', 'w') as f:
            f.write(self.scriptBox.toPlainText())

    def run_script(self):  # For running the main input script
        cursor = self.scriptBox.textCursor()  # Cursor of the input box
        cursor2 = QtGui.QTextCursor(self.outputBox.document())  # Cursor of the output box

        if cursor.hasSelection():  # If text is highlighted
            # Output highlighted text on the command line
            print(self.scriptBox.toPlainText()[cursor.selectionStart():cursor.selectionEnd()].strip())

            cursor2.beginEditBlock()
            cursor2.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)  # moves cursor to end
            cursor2.insertText(" Running partial script...\n>> ")  # Output that the partial script is running
            self.firstPos = cursor2.position()  # records first position of cursor line (for string output)
            cursor2.endEditBlock()

        else:
            print(self.scriptBox.toPlainText().strip())  # Output whole script on command line

            cursor2.beginEditBlock()
            cursor2.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
            cursor2.insertText(" Running script...\n>> ")  # Output that the whole script is running
            self.firstPos = cursor2.position()  # records first position of cursor line (for string output)
            cursor2.endEditBlock()

        self.savedPlainText = self.outputBox.toPlainText()  # Save the plain text
        self.savedHtmlText = self.outputBox.toHtml()  # Save the HTML (i.e. if text bolded, coloured etc)

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 1250, 700)
        self.setWindowTitle("MathChamp")

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

        # Output
        self.outputBox = QtWidgets.QTextEdit(self)
        self.outputBox.resize(990, 146)
        self.outputBox.move(25, 527)
        self.outputBox.setAlignment(Qt.AlignTop)  # Alignment of text
        self.outputBox.installEventFilter(self)  # Allows event detection

        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.insertText(">> ")
        self.firstPos = cursor.position()
        cursor.endEditBlock()

        self.savedHtmlText = self.outputBox.toHtml()
        self.savedPlainText = self.outputBox.toPlainText()

        table = QtWidgets.QTableWidget(self)
        table.setRowCount(100)
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Variable name", "Value"])
        table.setColumnWidth(0, 153) # indexing table at 0
        table.setColumnWidth(1, 153)
        table.resize(337, 447)
        table.move(887, 70)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)  # user can't edit variable table

        # Buttons
        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("RUN")
        self.b1.setIcon(QIcon('./ui/start.jpg'))
        self.b1.clicked.connect(self.run_script)  # runs text in script window
        self.b1.resize(70, 75)
        self.b1.move(1020, 522)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("STOP")
        self.b2.setIcon(QIcon('./ui/stop.jpg'))
        self.b2.clicked.connect(clicked)  # connected to a function
        self.b2.resize(70, 75)
        self.b2.move(1089, 522)

        self.plotButton = QtWidgets.QPushButton(self)
        self.plotButton.setText("PLOT")
        self.plotButton.clicked.connect(clicked)  # connected to a function
        self.plotButton.resize(70, 75)
        self.plotButton.move(1159, 522)

        self.b3 = QtWidgets.QPushButton(self)
        self.b3.setText("Create variable")
        self.b3.clicked.connect(self.show_variable_window)  # opens a new window
        self.b3.resize(210, 31)
        self.b3.move(1020, 592)

        self.an2 = QtWidgets.QPushButton(self)
        self.an2.setText("sin")
        self.an2.clicked.connect(self.sin)  # connected to a function
        self.an2.resize(50, 31)
        self.an2.move(1020, 619)

        self.an1 = QtWidgets.QPushButton(self)
        self.an1.setText("cos")
        self.an1.clicked.connect(self.cos)  # connected to a function
        self.an1.resize(50, 31)
        self.an1.move(1060, 619)

        self.b6 = QtWidgets.QPushButton(self)
        self.b6.setText("tan")
        self.b6.clicked.connect(self.tan)  # connected to a function
        self.b6.resize(50, 31)
        self.b6.move(1100, 619)

        self.b7 = QtWidgets.QPushButton(self)
        self.b7.setText("sqrt")
        self.b7.clicked.connect(self.sqrt)  # connected to a function
        self.b7.resize(50, 31)
        self.b7.move(1140, 619)

        self.b8 = QtWidgets.QPushButton(self)
        self.b8.setText("ln")
        self.b8.clicked.connect(self.ln)  # connected to a function
        self.b8.resize(50, 31)
        self.b8.move(1180, 619)

        self.an28 = QtWidgets.QPushButton(self)
        self.an28.setText("logx")
        self.an28.clicked.connect(self.logx)  # connected to a function
        self.an28.resize(50, 31)
        self.an28.move(1020, 646)

        self.an18 = QtWidgets.QPushButton(self)
        self.an18.setText("log10")
        self.an18.clicked.connect(self.log10)  # connected to a function
        self.an18.resize(50, 31)
        self.an18.move(1060, 646)

        self.b68 = QtWidgets.QPushButton(self)
        self.b68.setText("f(x)")
        self.b68.clicked.connect(self.fx)  # connected to a function
        self.b68.resize(50, 31)
        self.b68.move(1100, 646)

        self.b78 = QtWidgets.QPushButton(self)
        self.b78.setText("π")
        self.b78.clicked.connect(self.pi)  # connected to a function
        self.b78.resize(50, 31)
        self.b78.move(1140, 646)

        self.b88 = QtWidgets.QPushButton(self)
        self.b88.setText("e")
        self.b88.clicked.connect(self.exponent)  # connected to a function
        self.b88.resize(50, 31)
        self.b88.move(1180, 646)

        self.loadButton = QtWidgets.QPushButton(self)
        self.loadButton.setText("Load")
        #self.loadButton.clicked.connect(self.load)  # connected to a function
        self.loadButton.clicked.connect(self.show_load_window)
        self.loadButton.resize(60, 31)
        self.loadButton.move(820, 40)

        self.loadButton = QtWidgets.QPushButton(self)
        self.loadButton.setText("Save")
        self.loadButton.clicked.connect(self.show_save_window)  # connected to a function
        self.loadButton.resize(60, 31)
        self.loadButton.move(770, 40)

    def show_load_window(self):
        self.w = LoadWindow()
        self.w.show()

    def show_save_window(self):
        self.w = SaveWindow()
        self.w.show()

    def show_variable_window(self):
        self.w = VariableWindow()
        self.w.show()

    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.KeyPress and obj is self.outputBox:

            if event.key() == QtCore.Qt.Key_Backspace and self.outputBox.hasFocus():
                # String comparison stuff - next issue to tackle
                if ">> " == self.outputBox.toPlainText():

                    cursor = QtGui.QTextCursor(self.outputBox.document())
                    cursor.beginEditBlock()
                    cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
                    cursor.insertText("\n>> ")
                    cursor.endEditBlock()

                    self.outputBox.moveCursor(QtGui.QTextCursor.End)

                elif self.savedPlainText.strip() == self.outputBox.toPlainText().strip():
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

                    self.firstPos = self.lastPos
                    cursor.insertText("\n>> ")
                    cursor.endEditBlock()

                self.savedHtmlText = self.outputBox.toHtml()
                self.savedPlainText = self.outputBox.toPlainText()

        return super().eventFilter(obj, event)

class PlotWindow(QWidget):
    def __init__(self):
        super().__init__()

class SaveWindow(QWidget):
    def submit(self):
        # Use ReGex to employ data validation/verification
        # If self.input1 is not empty ect
        # Check that user hasn't already put .txt, otherwise remove it
        print(self.name.toPlainText()+".txt")
        self.close()

    def __init__(self):
        super().__init__()
        self.setGeometry(550, 370, 350, 110)  # Size of the window
        name = QtWidgets.QLabel(self)
        name.setText("<b>Save script</b>")
        font = name.font()
        font.setPointSize(20)
        name.setFont(font)
        name.move(115, 10)

        self.name = QtWidgets.QTextEdit(self)
        self.name.move(100, 40)
        self.name.resize(140,30)

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.submit)
        b1.move(125, 70)

class LoadWindow(QWidget):

    def submit(self):
        # Use ReGex to employ data validation/verification
        # If self.input1 is not empty ect
        print(self.comboBox.currentText())
        self.close()

    def __init__(self):
        super().__init__()
        self.setGeometry(550, 370, 350, 110)  # Size of the window
        name = QtWidgets.QLabel(self)
        name.setText("<b>Load script</b>")
        font = name.font()
        font.setPointSize(20)
        name.setFont(font)
        name.move(115, 10)

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.move(100, 40)
        self.comboBox.resize(140,30)

        # Not working atm - Not sure why (worked on mine)
        # Look into this
        onlyfiles = [f for f in listdir("./ui/scripts") if isfile(join(".", f))]
        print(onlyfiles)
        txtFiles = [f for f in onlyfiles if re.search("\.txt", f) != None]
        self.comboBox.addItems(txtFiles)

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.submit)
        b1.move(125, 70)


class VariableWindow(QWidget): # Variable Assignment Window - Have main window as input?
    def submit(self):
        # Use ReGex to employ data validation/verification
        # If self.input1 is not empty ect
        # Need to throw error and then print that out to screen
        print(self.input1.toPlainText() + " = " + self.input2.toPlainText())
        self.close()

    def __init__(self):
        super().__init__()

        self.setGeometry(550, 370, 350, 170) # Size of the window
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
        self.input1 = QtWidgets.QTextEdit(self)
        self.input1.move(125, 45)
        self.input1.resize(210, 30)
        self.input1.installEventFilter(self)  # Allows event detection


        name3 = QtWidgets.QLabel(self)
        name3.setText("Value:")
        font3 = name3.font()
        font3.setPointSize(15)
        name3.setFont(font3)
        name3.move(10, 87)
        self.input2 = QtWidgets.QTextEdit(self)
        self.input2.resize(210, 30)
        self.input2.move(125, 85)
        self.input2.installEventFilter(self)  # Allows event detection

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.submit)
        b1.move(120, 125)

# Needs development...
class Controller:
    def __init__(self):
        app = QApplication(sys.argv)
        self.show_main()
        sys.exit(app.exec_())

    def show_main(self):
        main = MainWindow()
        main.show()


def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()