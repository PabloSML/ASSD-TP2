from src.KarplusStrong.karplusStrong import karplus_strong
from src.KarplusStrong.karplusStrong import karplus_strong_drum
from src.Instrument import Instrument
import numpy as np
class ksGuitar(Instrument):
    def __init__(self):
        super(ksGuitar, self).__init__()
        pass

    def init_wavetable(self):
        """Generates a new wavetable for the string."""
        self.L = self.fs // int(self.noteFrequency)
        self.wavetable = (self.amplitude * 2 * np.random.randint(0, 2, self.L) - 1).astype(np.float)

    def play_note(self, noteFrequency, duration, fs, stretch_factor=1, amplitude=1):
        """Returns next sample from string."""
        self.noteFrequency = noteFrequency
        self.duration = duration
        self.fs = fs
        self.stretch_factor = stretch_factor
        self.amplitude = amplitude
        self.init_wavetable()
        self.sample = karplus_strong(self.wavetable, self.duration * self.fs, self.stretch_factor)
        return self.sample


class ksDrum(Instrument):
    def __init__(self):
        super(ksDrum, self).__init__()
        pass

    def init_wavetable(self):
        self.L = self.fs // int(self.noteFrequency)
        self.wavetable = (self.amplitude * 2 * np.random.randint(0, 2, self.L) - 1).astype(np.float)

    def play_note(self, noteFrequency, duration, fs, stretch_factor=1, amplitude=1):
        self.noteFrequency = noteFrequency
        self.duration = duration
        self.fs = fs
        self.stretch_factor = stretch_factor
        self.amplitude = amplitude
        self.init_wavetable()
        self.sample = karplus_strong_drum(self.wavetable, self.duration * self.fs)
        return self.sample