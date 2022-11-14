"""
Authors: Max, Paul, Chris, Ashwin and Sonya
Description: Function and value plotter
Version: V1.01
"""
import sys
from tkinter.ttk import Style
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvasQTAgg
from PyQt5.QtWidgets import QApplication, QWidget


"""User Input to be define"""
x_values = [1], 
y_values = [2]

"""Windows and Chart Formatting"""
fig = plt.figure("MathChamp")
plt.title("Expression")

plt.xlabel("X")
plt.ylabel("Y")

plt.plot(x_values, y_values, color="green")

plt.show()