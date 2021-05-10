from mido import MidiFile
import numpy as np


class TurnTable:

    def __init__(self, midi_file=None):
        self.midi_file = midi_file
        self.uspb_tempo_arr = []    # uspb = micro-sec per beat
        self.spt_tempo_arr = None   # spt = seconds per tick

    def load(self, midi_path=None):
        self.midi_file = MidiFile(midi_path)
        current_tick = 0

        for msg in self.midi_file.tracks[0]:
            current_tick += msg.time
            if msg.is_meta and msg.type == 'set_tempo':
                self.uspb_tempo_arr.append([current_tick, msg.tempo])
        self.uspb_tempo_arr = np.array(self.uspb_tempo_arr).T
        self.spt_tempo_arr = self.uspb_tempo_arr[1]/(1e6 * self.midi_file.ticks_per_beat)

    def current_spt_tempo(self, current_tick):
        return self.spt_tempo_arr[self.uspb_tempo_arr[0].searchsorted(current_tick) - 1]


phil = TurnTable()
phil.load('C:/Users/PabloSmolkin/PycharmProjects/ASSD-TP2/tests/StarWarsImperialMedley.mid')

