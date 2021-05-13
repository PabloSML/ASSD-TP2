from mido import MidiFile
import numpy as np
# import pandas as pd
from src.Track import Track
from src.SamAsh import SamAsh
import soundfile as sf
import pyaudio

class TurnTable:

    def __init__(self, midi_file=None):
        self.midi_file = midi_file
        self.trackList = []
        self.store = SamAsh()
        self.fs = 48000
        self.songLength = None
        self.song = None

    def load(self, midi_path=None):
        self.midi_file = MidiFile(midi_path)
        current_tick = 0
        uspb_tempos = []  # uspb = micro-sec per beat
        spt_tempos = None  # spt = seconds per tick

        for msg in self.midi_file.tracks[0]:
            current_tick += msg.time
            if msg.is_meta and msg.type == 'set_tempo':
                uspb_tempos.append([current_tick, msg.tempo])
        uspb_tempos = np.array(uspb_tempos).T
        spt_tempos = np.array([uspb_tempos[0], uspb_tempos[1]/(1e6 * self.midi_file.ticks_per_beat)])
        self.songLength = int(np.ceil(self.fs * self.midi_file.length))

        tracksCreated = 0
        for index, track in enumerate(self.midi_file.tracks[1:]):
            lastEv = track[-2]  # Sin contar End-Of-Track
            if lastEv.type.find('note') != -1 or lastEv.type.find('control') != -1:  # Ver que la track sea de notas
                self.trackList.append(Track(midiLength=self.songLength, midiTrack=track, trackNumber=index+1,
                                            spt_tempos=spt_tempos, store=self.store, fs=self.fs))
                self.trackList[tracksCreated].set_instrument('sampleGuitar')
                tracksCreated += 1
        # self.trackList[0].toggle_active()

    def set_fs(self, new_fs):
        self.fs = new_fs

    def synthesize(self):
        for track in self.trackList:
            if track.isActive:
                track.synthesize_track()
        print('Synthesized all tracks')

    def save_synthesis(self):
        self.song = np.zeros(self.songLength)
        for track in self.trackList:
            if track.isActive:
                if self.song.size < track.audioTrack.size:
                    self.song = np.append(self.song, np.zeros(track.audioTrack.size - self.song.size))
                self.song[:track.audioTrack.size] += track.audioTrack
        # if self.song.size < self.trackList[0].audioTrack.size:
        #     self.song = np.append(self.song, np.zeros(self.trackList[0].audioTrack.size - self.song.size))
        # self.song = self.trackList[0].audioTrack
        sf.write('D:/PycharmProjects/ASSD-TP2/tests/test.wav', self.song, self.fs)

beogram4000C = TurnTable()
beogram4000C.load('D:/PycharmProjects/ASSD-TP2/tests/rodriG.mid')
beogram4000C.synthesize()
beogram4000C.save_synthesis()
