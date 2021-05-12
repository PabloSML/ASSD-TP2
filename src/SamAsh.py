from src.SampleSynth.SampleInstruments import SampleViolin, SampleGuitar
from Instrument import GuitarString


class SamAsh:
    def __init__(self):
        self.availableInstruments = {'sampleViolin': SampleViolin, 'sampleGuitar': SampleGuitar,
                                     'guitarString': GuitarString}
        self.usedInstruments = {}

    def loan_instrument(self, instrument_name):
        if instrument_name in self.usedInstruments:
            return self.usedInstruments[instrument_name]
        else:
            new_instrument = self.availableInstruments[instrument_name]()
            self.usedInstruments[instrument_name] = new_instrument
            return new_instrument
