import sys
import ctypes.wintypes
from src.ui.mainwindow import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
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
        self.beogram4000C = TurnTable()

        # EVENT HANDLER: acciones a partir de la UI
        self.ui.load_button.clicked.connect(self.load_MIDI)

    def load_MIDI(self):
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        midiPath = QFileDialog.getOpenFileName(self, caption='Select MIDI File...', directory=buf.value, filter="MIDI Files (*.mid)")
        self.beogram4000C.load(midiPath[0])

        for index, track in enumerate(self.beogram4000C.trackList):
            tempObject = track_item(self, index + 1, track)
            tempItem = QtWidgets.QListWidgetItem()
            tempItem.setSizeHint(tempObject.sizeHint())
            self.ui.Tracklist.addItem(tempItem)
            self.ui.Tracklist.setItemWidget(tempItem, tempObject)