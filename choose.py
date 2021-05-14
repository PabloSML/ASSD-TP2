from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5 import QtGui
#from PyQt5.QtWidgets import QFrame, QMessageBox, QColorDialog
from src.ui.track import Ui_plotControlWrapper
from src.Track import Track
from select_popup import instrument_selector

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
            elif selection.drums_button.isChecked():
                self.instrument = 'drums'
            elif selection.flute_button.isChecked():
                self.instrument = 'flute'
            elif selection.violin_button.isChecked():
                self.instrument = 'violin'
            elif selection.trumpet_button.isChecked():
                self.instrument = 'trumpet'


            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("resources/designer/" + self.instrument + ".png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.instrument_button.setIcon(icon)