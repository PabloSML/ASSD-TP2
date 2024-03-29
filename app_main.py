import os
import ctypes.wintypes
from src.ui.mainwindow import Ui_Form
from choose import  track_item
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from src.AdditiveSynth.AdditiveSynthesizer import AddSynth
# from src.KarplusStrong.ksInstruments import ksGuitar
import pyaudio
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# Imports de backend
from src.TurnTable import TurnTable
from choose import track_item
import numpy as np
import time
from select_popup import instrument_selector

class AppClass(QtWidgets.QWidget):

    def __init__(self, parent=None):  # instanciamos la clase
        super(AppClass, self).__init__(parent)

        self.ui =Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("JacoBeats")
        self.ui.AllWidget.setCurrentIndex(0)

        # Icono
        myappid = 'jacobeats'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        app_icon = QtGui.QIcon()
        app_icon.addFile(os.path.dirname(__file__) + '/assets/keys.ico', QtCore.QSize(128, 128))
        self.setWindowIcon(app_icon)

        #Aca van las cosas que queres ocultar

        # MY STUFF: cosas que necesito instanciar externas a Qt

        # EVENT HANDLER:



        #Aca van las cosas que queres ocultar

        # MY STUFF: cosas que necesito instanciar externas a Qt
        self.beogram4000C = TurnTable()
        self.piano = AddSynth()
        self.pianoNote = np.array([])
        self.paObj = None
        self.player = None
        self.chunkSize = 1024
        self.chunkIndex = None
        self.playReady = False

        # EVENT HANDLER: acciones a partir de la UI
        self.ui.load_button.clicked.connect(self.load_MIDI)
        self.ui.Synth_button.clicked.connect(self.synth)
        self.ui.play_button.clicked.connect(self.play_pause)
        self.ui.stop_button.clicked.connect(self.stop_playback)
        self.ui.save_button.clicked.connect(self.master)

        self.ui.C_button.clicked.connect(self.play_C)
        self.ui.Db_button.clicked.connect(self.play_Db)
        self.ui.D_button.clicked.connect(self.play_D)
        self.ui.Eb_button.clicked.connect(self.play_Eb)
        self.ui.E_button.clicked.connect(self.play_E)
        self.ui.F_button.clicked.connect(self.play_F)
        self.ui.Gb_button.clicked.connect(self.play_Gb)
        self.ui.G_button.clicked.connect(self.play_G)
        self.ui.Ab_button.clicked.connect(self.play_Ab)
        self.ui.A_button.clicked.connect(self.play_A)
        self.ui.Bb_button.clicked.connect(self.play_Bb)
        self.ui.B_button.clicked.connect(self.play_B)
        self.ui.piano_select.clicked.connect(self.choose_instrument)


    def load_MIDI(self):
        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        midiPath = QFileDialog.getOpenFileName(self, caption='Select MIDI File...', directory=buf.value, filter="MIDI Files (*.mid)")

        if midiPath[0]:
            self.beogram4000C.load(midiPath[0])

            for index, track in enumerate(self.beogram4000C.trackList):
                tempObject = track_item(self, index + 1, track)
                tempItem = QtWidgets.QListWidgetItem()
                tempItem.setSizeHint(tempObject.sizeHint())
                self.ui.Tracklist.addItem(tempItem)
                self.ui.Tracklist.setItemWidget(tempItem, tempObject)

    def synth(self):
        msg = QMessageBox()
        msg.setWindowTitle('Beginning Synthesis...')
        msg.setText('The MIDI will begin synthesis when you press OK. Please be patient and tap your foot to some jams for better results')
        msgPopup = msg.exec_()
        self.beogram4000C.synthesize()
        self.playReady = True
        msg.setWindowTitle('Synthesis Complete')
        msg.setText('It\'s time to enjoy the grooves!')
        msgPopup = msg.exec_()

    def play_pause(self):
        if self.playReady:
            if self.ui.play_button.isChecked():
                self.start_playback()
            else:
                self.pause_playback()

    def start_playback(self):
        self.beogram4000C.start_playback()

    def pause_playback(self):
        self.beogram4000C.pause_playback()

    def stop_playback(self):
        if self.playReady:
            if self.ui.play_button.isChecked():
                self.ui.play_button.toggle()
            self.beogram4000C.stop_playback()

    def master(self):
        if self.playReady:
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            masterPath = QFileDialog.getSaveFileName(self, caption='Save Audio File...', directory=buf.value,
                                                   filter="WAV Files (*.wav);;FLAC Files (*.flac);;AIFF Files (*.aiff)")
            if masterPath[0]:
                self.beogram4000C.master(masterPath[0])

    def play_note(self, funNoteFreq):
        octave = self.ui.spinBox.value()
        noteFreq = funNoteFreq * 2**octave
        self.pianoNote = self.piano.play_note(freq=noteFreq, duration=1, fs=48000, instrument='piano', env='ADSR')[1]

        self.chunkIndex = 0

        if self.paObj is None:
            self.paObj = pyaudio.PyAudio()
        # abrimos player
        if self.player is None:
            self.player = self.paObj.open(rate=48000, channels=1, output=True, format=pyaudio.paFloat32, stream_callback=self.activate_awesome_player)

        if not self.player.is_active():
            self.player.start_stream()

        while self.player.is_active():
            time.sleep(0.01)

        self.player.stop_stream()
        self.player.close()
        self.paObj.terminate()
        self.player = None
        self.paObj = None

    def activate_awesome_player(self, in_data, frame_count, time_info, status):
        playbackData = np.zeros(self.chunkSize).astype(np.float32)

        chunkAudio = self.pianoNote[self.chunkIndex * self.chunkSize: (self.chunkIndex + 1) * self.chunkSize]
        playbackData[:chunkAudio.size] += chunkAudio

        sound = self.beogram4000C.prep_playback(playbackData)
        self.chunkIndex += 1
        if self.chunkIndex * self.chunkSize < self.pianoNote.size:
            return (sound, pyaudio.paContinue)
        else:
            self.chunkIndex = None
            return (sound, pyaudio.paComplete)

# Play Note Callbacks
    def choose_instrument(self):
        selection = instrument_selector()

        if selection.exec_():

            if selection.piano_button.isChecked():
                self.note_instrument = 'piano'
            elif selection.drums_button.isChecked():
                self.note_instrument = 'drums'
            elif selection.flute_button.isChecked():
                self.note_instrument = 'flute'
            elif selection.violin_button.isChecked():
                self.note_instrument = 'violin'
            elif selection.trumpet_button.isChecked():
                self.note_instrument = 'trumpet'

            icon = QtGui.QIcon()
            prePath = os.path.dirname(__file__).replace('\\', '/') + '/'
            icon.addPixmap(QtGui.QPixmap(prePath + 'assets/' + self.note_instrument + ".png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.ui.piano_select.setIcon(icon)



    def play_C(self):
        self.play_note(16.35)
    def play_Db(self):
        self.play_note(17.32)
    def play_D(self):
        self.play_note(18.35)
    def play_Eb(self):
        self.play_note(19.0)
    def play_E(self):
        self.play_note(20.3)
    def play_F(self):
        self.play_note(21.83)
    def play_Gb(self):
        self.play_note(23.12)
    def play_G(self):
        self.play_note(24.5)
    def play_Ab(self):
        self.play_note(25.96)
    def play_A(self):
        self.play_note(27.5)
    def play_Bb(self):
        self.play_note(29.0)
    def play_B(self):
        self.play_note(30.87)
