import sys
from src.ui.mainwindow import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
# from src import UniFilter as UF
# from src.lib import handy as hand
# from src.lib.PlotControl import plotControl
import numpy as np
import scipy.signal as ss


class AppClass(QtWidgets.QWidget):

    def __init__(self, parent=None):  # instanciamos la clase
        super(AppClass, self).__init__(parent)

        self.ui =Ui_Form()
        self.ui.setupUi(self)


        #Aca van las cosas que queres ocultar

        # MY STUFF: cosas que necesito instanciar externas a Qt

        # EVENT HANDLER: acciones a partir de la UI




