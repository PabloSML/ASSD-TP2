from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import QtGui
#from PyQt5.QtWidgets import QFrame, QMessageBox, QColorDialog
from src.ui.track import Ui_plotControlWrapper
from src.Track import Track
from select_popup import instrument_selector
import os

class track_item(QWidget, Ui_plotControlWrapper):

    def __init__(self, mainWindow, i, track: Track):
        super(track_item, self).__init__()
        self.setupUi(self)
        self.mainWindow = mainWindow
        self.name = 'Track ' + str(i)
        self.track_label.setText(self.name)
        self.track = track

        #Y STUFF: cosas que necesito instanciar externas a Qt
        self.volume_slider.setValue(self.volume_slider.maximum())

        #EVENT HANDLER
        self.instrument_button.pressed.connect(self.open_popup)
        self.mute_button.pressed.connect(self.toggle_mute)
        self.volume_slider.valueChanged.connect(self.update_volume)

    def update_volume(self):
        newVolume = self.volume_slider.value() / self.volume_slider.maximum()
        self.track.set_volume(newVolume)

    def toggle_mute(self):
        self.track.toggle_active()

    def open_popup(self):

        selection = instrument_selector()

        if selection.exec_():

            if selection.piano_button.isChecked():
                self.instrument = 'piano'
                self.track.set_instrument('piano', additive=True)
            elif selection.drums_button.isChecked():
                self.instrument = 'drums'
                self.track.set_instrument('ksDrum')
            elif selection.flute_button.isChecked():
                self.instrument = 'flute'
                self.track.set_instrument('flute', additive=True)
            elif selection.violin_button.isChecked():
                self.instrument = 'violin'
                self.track.set_instrument('violin', additive=True)
            elif selection.trumpet_button.isChecked():
                self.instrument = 'trumpet'
                self.track.set_instrument('trumpet', additive=True)
            elif selection.guitar_button.isChecked():
                self.instrument = 'guitar'
                self.track.set_instrument('ksGuitar')


            icon = QtGui.QIcon()
            prePath = os.path.dirname(__file__).replace('\\', '/') + '/'
            icon.addPixmap(QtGui.QPixmap(prePath + "assets/" + self.instrument + ".png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.instrument_button.setIcon(icon)