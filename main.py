"""
Author:      Max James

Date:        10/01/23

Description: The graphical user interface for the maths interpreter software. This works by taking strings from the input
             boxes and then feeding them into the interpreter (going through the lexer, parser, and execution pass).
             Additionally, there is a way to display plots with the 'f(x)' button, which again users our own interpreter
             to calculate each plot and then uses the Matplotlib library to display the plot.

             Additional features for the GUI include being able to write, save, and load scripts and to clear the values
             on the output box. All variables will also be displayed on the right hand table, showing the current value
             of the variable. Additionally, there is a window that appears for assignment a variable. This works by
             taking the input in the boxes and then sending them to the "output" box for execution once enter is pressed.
             This exists to restrict user input, to avoid misinput (data validation using ReGex). There are additionally
             extra windows for opening a file, saving a file, and for writing in the f(x) function before displaying the
             Matplotlib plot.

Version:     V5

History:     V1 - Basic layout for main window of GUI made
             V1.1 - Basic outline for variable assignment window made
             V1.2 - Save and load buttons added, alongside windows
             V1.3 - Bug fixes to the code
             V2 - GUI is linked to the interpreter code previously made
             V2.1 - Bug fixes to the code
             V3 - Implementing the ability to add a plot
             V3.1 - Data validation added for all the windows (might need to update for save window)
             V4 - Variable dependencies added
             V4.1 - Small bug fixes to the variable dependencies, removing dependencies when re-defined
             V4.2 - Made changes to PlotInputWindow, to include intervals
             V4.3 - Variables output, Y-Axis now stationary, Stylesheet changed
             V4.4 - Updated values to account for new Stylesheet used
             V5 - Code fully cleaned up and everything working as planned, even on Windows machines

References: https://stackoverflow.com/questions/15263063/why-keypress-event-in-pyqt-does-not-work-for-key-enter
            https://stackoverflow.com/questions/72169262/pyqt5-access-mainwindow-from-another-window
            https://www.geeksforgeeks.org/pyqt5-qtablewidget/
            https://zetcode.com/gui/pyqt5/layout/
            https://doc.qt.io/qtforpython/overviews/layout.html
            https://matplotlib.org/3.3.4/gallery/recipes/placing_text_boxes.html
"""

from core.interpreter import Interpreter
from core.lexer.lexicalAnalyzer import Lexer
from core.lexer.token import TokenType
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from os import listdir
import sys
import matplotlib.pyplot as plt
import numpy as np
import re


class PlotWindow:
    def __init__(self, function):
        print(function)

        function = function.split("|")

        # linearly spaced numbers from 'function[1]' to 'function[2]'
        x = np.linspace(int(function[1]), int(function[2]), 100)  # 100 of these values
        y = np.zeros(100)  # y list of the same length

        __tokens = Lexer(
            function[0]
        ).get_tokens()  # get the tokens of inputted function

        for i in range(len(x)):
            string_build = ""  # builds string that's read into interpreter
            for z in range(len(__tokens)):  # for every token in string

                if (
                    __tokens[z].type == TokenType.IDENTIFIER
                ):  # if token is an identifier

                    if __tokens[z].value != "x":  # if identifier is 'x'
                        # replace with variable value
                        string_build = (
                            string_build
                            + "("
                            + str(Interpreter(__tokens[z].value).execute())
                            + ")"
                        )
                    else:
                        string_build = (
                            string_build + "(" + str(x[i]) + ")"
                        )  # replace value within 'x' list

                elif (
                    __tokens[z].type == TokenType.INTEGER
                    or __tokens[z].type == TokenType.FLOAT
                ):
                    # puts numbers in brackets to ensure BODMAS
                    string_build = string_build + "(" + str(__tokens[z].value) + ")"
                else:  # if it's not any of the three aformentioned token types
                    string_build = string_build + __tokens[z].value.replace(
                        "'", ""
                    )  # add to string

            # print(string_build)
            y[i] = Interpreter(
                string_build
            ).execute()  # calculate and add to y at correct index

        # setting the axes at the centre
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.spines["left"].set_position("zero")
        ax.spines["bottom"].set_position("zero")
        ax.spines["right"].set_color("none")
        ax.spines["top"].set_color("none")
        ax.xaxis.set_ticks_position("bottom")
        ax.yaxis.set_ticks_position("left")

        text_box = "Zero crossings = "
        props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
        ax.text(
            0.05,
            0.95,
            text_box,
            transform=ax.transAxes,
            fontsize=14,
            verticalalignment="top",
            bbox=props,
        )

        # plot the function
        plt.plot(x, y, "r")
        plt.title("Plot for " + function[0])

        plt.grid()

        # show the plot
        plt.show()


class PlotInputWindow(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(550, 370, 350, 165)  # Size of the window
        self.setFixedSize(350, 165)

        title = QLabel(self)
        pixmap = QPixmap("./ui/images/plot1.jpg")
        title.setPixmap(
            pixmap.scaled(90, 90, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        title.move(123, 14)

        assignments = QLabel(self)
        pixmap = QPixmap("./ui/images/plot2.jpg")
        assignments.setPixmap(
            pixmap.scaled(70, 70, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        assignments.move(43, 50)

        to_label = QLabel(self)
        pixmap = QPixmap("./ui/images/plot4.jpg")
        to_label.setPixmap(
            pixmap.scaled(16, 16, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        to_label.move(151, 85)

        self.inputBox = QtWidgets.QTextEdit(self)
        self.inputBox.move(120, 40)
        self.inputBox.resize(140, 30)

        self.inputBox_left = QtWidgets.QTextEdit(self)
        self.inputBox_left.move(120, 75)
        self.inputBox_left.resize(30, 30)

        self.inputBox_right = QtWidgets.QTextEdit(self)
        self.inputBox_right.move(170, 75)
        self.inputBox_right.resize(30, 30)

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.switch)
        b1.move(125, 110)

        self.error = QLabel(self)
        pixmap = QPixmap("./ui/images/plot3.jpg")
        self.error.setPixmap(
            pixmap.scaled(130, 130, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        self.error.move(100, 140)
        self.error.setVisible(False)  # Initially set as False, unless error occurs

    def switch(self):
        self.switch_window.emit(
            self.inputBox.toPlainText()
            + "|"
            + self.inputBox_left.toPlainText()
            + "|"
            + self.inputBox_right.toPlainText()
        )


class SaveWindow(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(550, 370, 350, 130)  # Size of the window
        self.setFixedSize(350, 130)

        name_label = QLabel(self)
        pixmap = QPixmap("./ui/images/save1.jpg")
        name_label.setPixmap(
            pixmap.scaled(110, 110, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        name_label.move(113, 13)

        self.name = QtWidgets.QTextEdit(self)
        self.name.move(100, 40)
        self.name.resize(140, 30)

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.switch)
        b1.move(125, 80)

        self.error = QLabel(self)
        pixmap = QPixmap("./ui/images/save2.jpg")
        self.error.setPixmap(
            pixmap.scaled(190, 190, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        self.error.move(70, 110)
        self.error.setVisible(False)  # Initially set as False, unless error occurs

    def switch(self):
        if (
            re.search(r"^[a-zA-Z0-9]*$", self.name.toPlainText()) == None
        ):  # if there is a space
            self.error.setVisible(True)
        else:
            self.switch_window.emit(self.name.toPlainText() + ".txt")


class LoadWindow(QtWidgets.QWidget):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(550, 370, 350, 130)  # Size of the window
        self.setFixedSize(350, 130)

        name_label = QLabel(self)
        pixmap = QPixmap("./ui/images/load1.jpg")
        name_label.setPixmap(
            pixmap.scaled(110, 110, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        name_label.move(113, 13)

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.move(100, 40)
        self.comboBox.resize(140, 30)

        onlyfiles = [f for f in listdir("./ui/scripts/")]
        txtFiles = [f for f in onlyfiles if re.search("\.txt", f) != None]
        self.comboBox.addItems(txtFiles)

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.select)
        b1.move(125, 80)

        self.error = QLabel(self)
        pixmap = QPixmap("./ui/images/load2.jpg")
        self.error.setPixmap(
            pixmap.scaled(190, 190, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        self.error.move(70, 110)
        self.error.setVisible(False)  # Initially set as False, unless error occurs

    def select(self):
        if self.comboBox.currentText().strip() == "":
            self.error.setVisible(True)
        else:
            self.switch_window.emit(self.comboBox.currentText())


class VariableWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(550, 370, 350, 190)  # Size of the window
        self.setFixedSize(350, 190)

        name_label = QLabel(self)
        pixmap = QPixmap("./ui/images/var1.jpg")
        name_label.setPixmap(
            pixmap.scaled(190, 190, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        name_label.move(83, 13)

        assignments = QLabel(self)
        pixmap = QPixmap("./ui/images/var2.jpg")
        assignments.setPixmap(
            pixmap.scaled(115, 115, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        assignments.move(5, 52)

        self.input1 = QtWidgets.QLineEdit(self)
        self.input1.move(125, 45)
        self.input1.resize(210, 30)
        self.input1.installEventFilter(self)  # Allows event detection

        self.input2 = QtWidgets.QLineEdit(self)
        self.input2.resize(210, 30)
        self.input2.move(125, 85)
        self.input2.installEventFilter(self)  # Allows event detection

        b1 = QtWidgets.QPushButton(self)
        b1.setText("Submit")
        b1.clicked.connect(self.switch)
        b1.move(120, 125)

        self.error = QLabel(self)
        pixmap = QPixmap("./ui/images/var3.jpg")
        self.error.setPixmap(
            pixmap.scaled(160, 160, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        self.error.move(80, 160)
        self.error.setVisible(False)  # Initially set as False, unless error occurs

    def switch(self):
        text = self.input1.text() + "=" + self.input2.text()
        try:
            Interpreter(text).execute()
            self.switch_window.emit(self.input1.text() + "=" + self.input2.text())
        except:
            self.error.setVisible(True)


class MainWindow(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()
    switch_window2 = QtCore.pyqtSignal()
    switch_window3 = QtCore.pyqtSignal()
    switch_window4 = QtCore.pyqtSignal()

    def __init__(
        self,
        text,
        outputText,
        scriptText,
        pos,
        varHold,
        varDec,
        varDep,
        var,
        save,
        load,
    ):
        QtWidgets.QWidget.__init__(self)
        self.setGeometry(100, 100, 1250, 700)
        self.setFixedSize(1250, 700)
        self.setWindowTitle("MathChamp")

        # might need to be changed later
        self.varDec = varDec  # needs to be stored early
        self.varDependencies = varDep

        self.varDict = varHold  # dictionary to hold the variables
        self.linePos = (
            -1
        )  # Should be -1 (unless loading after sub-window - need to do more)

        name = QLabel(self)
        pixmap = QPixmap("./ui/images/mctext.jpg")
        name.setPixmap(
            pixmap.scaled(300, 300, aspectRatioMode=QtCore.Qt.KeepAspectRatio)
        )
        name.move(80, 0)

        # Label at the top of application
        label = QLabel(self)
        pixmap = QPixmap("./ui/images/logo.jpg")
        label.setPixmap(pixmap.scaled(55, 55))
        label.adjustSize()
        label.move(26, 7)

        # Scripting box
        self.scriptBox = QtWidgets.QTextEdit(self)
        self.scriptBox.resize(841, 448)
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
        self.outputBox.move(25, 529)
        self.outputBox.setAlignment(Qt.AlignTop)  # Alignment of text
        self.outputBox.installEventFilter(self)  # Allows event detection

        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()

        if var != None:  # variable window text
            cursor.insertText(text)

        if save != None:
            with open("./ui/scripts/" + text, "w") as f:  # Need to fix
                f.write(self.scriptBox.toPlainText())

            self.outputBox.setText(outputText)

        if load != None:
            with open("./ui/scripts/" + text, "r") as f:
                self.scriptBox.setText(f.read())

            self.outputBox.setText(outputText)

        if (self.outputBox.toPlainText() + text) == ">> ":
            cursor.insertText(text)

        self.firstPos = cursor.position() - 1

        if self.firstPos != 3:
            self.firstPos = pos

        cursor.endEditBlock()

        self.savedHtmlText = self.outputBox.toHtml()
        self.savedPlainText = self.outputBox.toPlainText()

        # Variable table
        self.table = QtWidgets.QTableWidget(self)
        self.table.setRowCount(100)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Variable name", "Value"])
        self.table.setColumnWidth(0, 153)  # indexing table at 0
        self.table.setColumnWidth(1, 153)
        self.table.resize(347, 447)
        self.table.move(877, 70)
        self.table.setEditTriggers(
            QtWidgets.QTableWidget.NoEditTriggers
        )  # user can't edit variable table

        # Buttons
        self.runButton = QtWidgets.QPushButton(self)
        self.runButton.setText("RUN")
        self.runButton.setIcon(QIcon("./ui/images/start.jpg"))
        self.runButton.clicked.connect(self.run_script)  # runs text in script window
        self.runButton.resize(95, 65)
        self.runButton.move(1027, 528)

        self.plotButton = QtWidgets.QPushButton(self)
        self.plotButton.setText("f(x)")
        self.plotButton.clicked.connect(self.plot)  # connected to a function
        self.plotButton.resize(95, 65)
        self.plotButton.move(1129, 528)

        self.varButton = QtWidgets.QPushButton(self)
        self.varButton.setText("Create variable")
        self.varButton.clicked.connect(self.variable)
        self.varButton.resize(197, 21)
        self.varButton.move(1027, 602)

        self.sinButton = QtWidgets.QPushButton(self)
        self.sinButton.setText("sin")
        self.sinButton.clicked.connect(self.sin)  # connected to a function
        self.sinButton.resize(41, 41)
        self.sinButton.move(1027, 632)

        self.cosButton = QtWidgets.QPushButton(self)
        self.cosButton.setText("cos")
        self.cosButton.clicked.connect(self.cos)  # connected to a function
        self.cosButton.resize(40, 41)
        self.cosButton.move(1067, 632)

        self.tanButton = QtWidgets.QPushButton(self)
        self.tanButton.setText("tan")
        self.tanButton.clicked.connect(self.tan)  # connected to a function
        self.tanButton.resize(40, 41)
        self.tanButton.move(1106, 632)

        self.sqrtButton = QtWidgets.QPushButton(self)
        self.sqrtButton.setText("fact")
        self.sqrtButton.clicked.connect(self.factorial)  # connected to a function
        self.sqrtButton.resize(40, 41)
        self.sqrtButton.move(1145, 632)

        self.lnButton = QtWidgets.QPushButton(self)
        self.lnButton.setText("π")
        self.lnButton.clicked.connect(self.pi)  # connected to a function
        self.lnButton.resize(40, 41)
        self.lnButton.move(1184, 632)

        self.loadButton = QtWidgets.QPushButton(self)
        self.loadButton.setText("Load")
        self.loadButton.clicked.connect(self.load)  # connected to a function
        self.loadButton.resize(45, 21)
        self.loadButton.move(820, 45)  # 1180

        self.saveButton = QtWidgets.QPushButton(self)
        self.saveButton.setText("Save")
        self.saveButton.clicked.connect(self.save)  # connected to a function
        self.saveButton.resize(45, 21)
        self.saveButton.move(770, 45)  # 820

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

    def pi(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("3.141592653589793238")
        cursor.endEditBlock()

    def factorial(self):
        cursor = QtGui.QTextCursor(self.outputBox.document())
        cursor.beginEditBlock()
        cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)

        self.lastPos = cursor.position()
        self.firstPos = self.lastPos
        cursor.insertText("fact()")
        cursor.endEditBlock()

    def run_script(self):  # For running the main input script
        cursor = self.scriptBox.textCursor()  # Cursor of the input box
        cursor2 = QtGui.QTextCursor(
            self.outputBox.document()
        )  # Cursor of the output box

        if cursor.hasSelection():  # If text is highlighted
            # Output highlighted text on the command line
            selected = self.scriptBox.toPlainText()[
                cursor.selectionStart() : cursor.selectionEnd()
            ].strip()
            script_type = "Running partial script...\n"

        else:
            selected = (
                self.scriptBox.toPlainText().strip()
            )  # Output whole script on command line
            script_type = "Running script...\n"

        cursor2.beginEditBlock()
        cursor2.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        cursor2.insertText(script_type)  # Output that the whole script is running

        for line in selected.splitlines():
            cursor2.movePosition(
                QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor
            )  # moves cursor to end
            cursor2.insertText(">> " + line + "\n")
            try:
                Interpreter(line).execute()
                __tokens = Lexer(line).get_tokens()

                if len(__tokens) > 1:
                    if (
                        __tokens[0].type == TokenType.IDENTIFIER
                        and __tokens[1].type == TokenType.ASSIGN
                    ):

                        cursor2.insertText(str(Interpreter(line).execute()) + "\n")

                        if __tokens[0].value not in list(self.varDict.keys()):
                            self.varDependencies[__tokens[0].value] = []
                        else:
                            print(__tokens[0].value)
                            for i in self.varDependencies[__tokens[0].value]:
                                print(i)
                                print(Interpreter(self.varDec[i]).execute())
                                self.varDict[i] = Interpreter(self.varDec[i]).execute()

                        self.varDict[__tokens[0].value] = str(
                            Interpreter(line).execute()
                        )

                        if __tokens[0].value in self.varDec.keys():
                            for i in self.varDependencies:
                                if __tokens[0].value in self.varDependencies[i]:
                                    self.varDependencies[i].remove(__tokens[0].value)

                        self.varDec[
                            __tokens[0].value
                        ] = line  # stores the assignment line of variable

                        for i in range(len(__tokens[2:])):
                            if TokenType.IDENTIFIER == __tokens[i + 2].type:
                                if (
                                    __tokens[0].value
                                    not in self.varDependencies[__tokens[i + 2].value]
                                ):
                                    self.varDependencies[__tokens[i + 2].value].append(
                                        __tokens[0].value
                                    )

                        for i in range(len(self.varDict.keys())):
                            self.table.setItem(
                                i,
                                0,
                                QtWidgets.QTableWidgetItem(
                                    list(self.varDict.keys())[i]
                                ),
                            )
                            self.table.setItem(
                                i,
                                1,
                                QtWidgets.QTableWidgetItem(
                                    str(self.varDict.get(list(self.varDict.keys())[i]))
                                ),
                            )

                    else:
                        cursor2.insertText(str(Interpreter(line).execute()) + "\n")

                else:
                    cursor2.insertText(str(Interpreter(line).execute()) + "\n")

            except:
                cursor2.insertText(
                    "ERROR: Issue at line "
                    + str(selected.splitlines().index(line) + 1)
                    + "\n"
                )
                break

        cursor2.insertText(">> ")
        self.firstPos = (
            cursor2.position()
        )  # records first position of cursor line (for string output)
        cursor2.endEditBlock()

        self.savedPlainText = self.outputBox.toPlainText()  # Save the plain text
        self.savedHtmlText = (
            self.outputBox.toHtml()
        )  # Save the HTML (i.e. if text bolded, coloured etc)

    def variable(self):
        self.switch_window.emit()

    def save(self):
        self.switch_window2.emit()

    def load(self):
        self.switch_window3.emit()

    def plot(self):
        self.switch_window4.emit()

    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.KeyPress and obj is self.outputBox:

            if event.key() == QtCore.Qt.Key_Backspace and self.outputBox.hasFocus():

                if self.savedPlainText.strip() == self.outputBox.toPlainText().strip():
                    cursor = QtGui.QTextCursor(self.outputBox.document())
                    cursor.beginEditBlock()
                    cursor.movePosition(
                        QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor
                    )
                    cursor.insertText("\n>> ")
                    cursor.endEditBlock()

                    self.outputBox.setText(self.savedHtmlText)
                    self.outputBox.moveCursor(QtGui.QTextCursor.End)

            if event.key() == QtCore.Qt.Key_Return and self.outputBox.hasFocus():
                self.savedHtmlText = self.outputBox.toHtml()

                cursor = QtGui.QTextCursor(self.outputBox.document())
                cursor.beginEditBlock()
                cursor.movePosition(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
                self.lastPos = cursor.position()

                line = (
                    self.outputBox.toPlainText()[self.firstPos : self.lastPos]
                    .replace(">>", "")
                    .strip()
                )

                if line == "clear":
                    self.outputBox.setText("")
                    cursor.insertText(">> ")
                    self.firstPos = cursor.position()
                    cursor.endEditBlock()
                else:
                    try:
                        execution = Interpreter(line).execute()
                        cursor.insertText("\n" + str(execution))

                        __tokens = Lexer(line).get_tokens()

                        if len(__tokens) > 1:
                            if (
                                __tokens[0].type == TokenType.IDENTIFIER
                                and __tokens[1].type == TokenType.ASSIGN
                            ):

                                # if not already in dictionary keys:
                                if __tokens[0].value not in list(self.varDict.keys()):
                                    self.varDependencies[__tokens[0].value] = []
                                else:  # need to execute for dependencies
                                    for i in self.varDependencies[__tokens[0].value]:
                                        self.varDict[i] = Interpreter(
                                            self.varDec[i]
                                        ).execute()

                                self.varDict[__tokens[0].value] = str(execution)

                                if __tokens[0].value in self.varDec.keys():
                                    for i in self.varDependencies:
                                        if __tokens[0].value in self.varDependencies[i]:
                                            self.varDependencies[i].remove(
                                                __tokens[0].value
                                            )

                                self.varDec[
                                    __tokens[0].value
                                ] = line  # stores the assignment line of variable

                                for i in range(len(__tokens[2:])):

                                    # i+2 to not include the identifier at the start of assignment
                                    if (
                                        TokenType.IDENTIFIER == __tokens[i + 2].type
                                    ):  # if there is another variable after assign
                                        if (
                                            __tokens[0].value
                                            not in self.varDependencies[
                                                __tokens[i + 2].value
                                            ]
                                        ):  # if not already in list
                                            self.varDependencies[
                                                __tokens[i + 2].value
                                            ].append(
                                                __tokens[0].value
                                            )  # add to list for variables

                                # Adding dictionary values to graphical table
                                for i in range(len(self.varDict.keys())):
                                    self.table.setItem(
                                        i,
                                        0,
                                        QtWidgets.QTableWidgetItem(
                                            list(self.varDict.keys())[i]
                                        ),
                                    )
                                    self.table.setItem(
                                        i,
                                        1,
                                        QtWidgets.QTableWidgetItem(
                                            str(
                                                self.varDict.get(
                                                    list(self.varDict.keys())[i]
                                                )
                                            )
                                        ),
                                    )

                    except Exception as e:
                        cursor.insertText("\nERROR: " + str(e))

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
    varDict = {}
    varDec = {}
    varDependencies = {}

    def __init__(self):
        pass

    def show_main(self, text=">> "):

        # Closing sub-windows if they're open
        try:
            self.window.close()
        except:
            self.window = None

        try:
            # IN DEVELOPMENT
            if (
                re.search(r"^[a-zA-Z0-9]*$", self.saveWin.name.toPlainText()) == None
            ):  # if there is a space
                self.saveWin.error.setVisible(True)
        except:
            self.saveWin = None

        try:
            self.loadWin.close()
        except:
            self.loadWin = None

        if self.window != None:
            self.outputBoxText = self.main.savedPlainText
            text = self.outputBoxText + text

        self.main = MainWindow(
            text,
            self.outputBoxText,
            self.inputBoxText,
            self.pos,
            self.varDict,
            self.varDec,
            self.varDependencies,
            self.window,
            self.saveWin,
            self.loadWin,
        )
        self.window = None
        self.saveWin = None
        self.loadWin = None

        for i in range(len(self.varDict.keys())):
            self.main.table.setItem(
                i, 0, QtWidgets.QTableWidgetItem(list(self.varDict.keys())[i])
            )
            self.main.table.setItem(
                i,
                1,
                QtWidgets.QTableWidgetItem(
                    str(self.varDict.get(list(self.varDict.keys())[i]))
                ),
            )

        self.main.switch_window.connect(self.show_var)
        self.main.switch_window2.connect(self.show_save)
        self.main.switch_window3.connect(self.show_load)
        self.main.switch_window4.connect(self.show_pinput)

        self.main.show()

    def show_pinput(self):
        self.pinputWin = PlotInputWindow()

        self.outputBoxText = self.main.savedPlainText
        self.inputBoxText = self.main.scriptBox.toPlainText()
        self.pos = self.main.firstPos
        self.varDict = self.main.varDict

        self.varDependencies = self.main.varDependencies
        self.varDec = self.main.varDec

        self.pinputWin.switch_window.connect(self.show_plot)
        self.pinputWin.show()

    def show_plot(self, text):

        self.outputBoxText = self.main.savedPlainText
        self.inputBoxText = self.main.scriptBox.toPlainText()
        self.pos = self.main.firstPos
        self.varDict = self.main.varDict

        self.varDependencies = self.main.varDependencies
        self.varDec = self.main.varDec

        try:
            self.pinputWin.error.setVisible(False)
            self.plotWin = PlotWindow(text)
        except:
            self.pinputWin.error.setVisible(True)

    def show_var(self):
        self.window = VariableWindow()

        self.outputBoxText = self.main.savedPlainText
        self.inputBoxText = self.main.scriptBox.toPlainText()
        self.pos = self.main.firstPos
        self.varDict = self.main.varDict

        self.varDependencies = self.main.varDependencies
        self.varDec = self.main.varDec

        self.window.switch_window.connect(self.show_main)
        self.window.show()

    def show_save(self):
        self.saveWin = SaveWindow()

        self.outputBoxText = self.main.savedPlainText
        self.inputBoxText = self.main.scriptBox.toPlainText()
        self.pos = self.main.firstPos
        self.varDict = self.main.varDict

        self.varDependencies = self.main.varDependencies
        self.varDec = self.main.varDec

        self.saveWin.switch_window.connect(self.show_main)
        self.saveWin.show()

    def show_load(self):
        self.loadWin = LoadWindow()

        self.outputBoxText = self.main.savedPlainText
        self.inputBoxText = self.main.scriptBox.toPlainText()
        self.pos = self.main.firstPos
        self.varDict = self.main.varDict

        self.varDependencies = self.main.varDependencies
        self.varDec = self.main.varDec

        self.loadWin.switch_window.connect(self.show_main)
        self.loadWin.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    controller = Controller()
    controller.show_main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
