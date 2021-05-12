
class Instrument:
    def __init__(self):
        pass

    def play_note(self, noteFrequency, duration, fs, **kwargs):
        raise Exception('play_note function must be overwritten for Instrument child')

