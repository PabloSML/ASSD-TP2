from mido import MidiFile
import numpy as np
from src.Track import Track
from src.SamAsh import SamAsh


class TurnTable:

    def __init__(self, midi_file=None):
        self.midi_file = midi_file
        self.trackList = []
        self.store = SamAsh()

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

        for track in self.midi_file.tracks[1:]:
            self.trackList.append(Track(midiTrack=track, spt_tempos=spt_tempos, store=self.store))

        self.trackList[0].set_instrument('sampleSynth')
        self.trackList[0].toggle_active()

    def synthesize(self):
        for track in self.trackList:
            if track.isActive:
                track.synthesize_track()

beogram4000C = TurnTable()
beogram4000C.load('C:/Users/PabloSmolkin/PycharmProjects/ASSD-TP2/tests/StarWarsImperialMedley.mid')
beogram4000C.synthesize()

