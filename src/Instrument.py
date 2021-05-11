from src.karplusStrong import karplus_strong

class Instrument:
    def __init__(self):
        pass

    def play_note(self, noteFrequency, duration, fs, **kwargs):
        raise Exception('play_note function must be overwritten for Instrument child')


class GuitarString(Instrument):
    def __init__(self):
        super(GuitarString, self).__init__()
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