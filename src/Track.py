from mido import MidiFile
from src.SamAsh import SamAsh
from src.Instrument import Instrument
from src.SampleSynth import SampleSynth


class Track:
    def __init__(self, midiTrack = None, spt_tempos=None, store: SamAsh = None):
        self.midiTrack = midiTrack
        self.spt_tempos = spt_tempos
        self.audioTrack = None
        self.isActive = False
        self.store = store
        self.instrument = None

    def toggle_active(self):
        self.isActive = not self.isActive

    def set_instrument(self, instrument_name):
        self.instrument = self.store.loan_instrument(instrument_name)

    def current_spt_tempo(self, current_tick):
        return self.spt_tempos[1][self.spt_tempos[0].searchsorted(current_tick) - 1]

    def synthesize_track(self):
        print(self.current_spt_tempo(40000))
