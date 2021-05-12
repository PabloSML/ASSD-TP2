from src.Instrument import Instrument
import src.SampleSynth.sample_synth as ssynth
import soundfile as sf


class SampleViolin(Instrument):
    def __init__(self):
        super(SampleViolin, self).__init__()
        self.samplesPath = 'C:/Users/PabloSmolkin/PycharmProjects/ASSD-TP2/src/SampleSynth/Violin/'

    def play_note(self, noteFrequency, duration, fs, **kwargs):
        noteNumber = kwargs['noteNumber']
        note = None

        if noteNumber in range(55, 109, 1):
            sample, sample_fs = sf.read(self.samplesPath + str(noteNumber) + '.aif')
            middleChannel = ssynth.averageChannels(sample)
            note = middleChannel

        elif noteNumber < 55:
            semitonalDiff = noteNumber - 55
            sample, sample_fs = sf.read(self.samplesPath + '55.aif')
            middleChannel = ssynth.averageChannels(sample)
            note = ssynth.pitchShift(middleChannel, 1024, 256, semitonalDiff)

        else:
            semitonalDiff = noteNumber - 108
            sample, sample_fs = sf.read(self.samplesPath + '108.aif')
            middleChannel = ssynth.averageChannels(sample)
            note = ssynth.pitchShift(middleChannel, 1024, 256, semitonalDiff)

        sample_len = note.size/sample_fs
        timeFactor = duration/sample_len

        note = ssynth.timeScaler(note, 1024, 256, timeFactor)

        return note


class SampleGuitar(Instrument):
    def __init__(self):
        super(SampleGuitar, self).__init__()
        self.samplesPath = 'C:/Users/PabloSmolkin/PycharmProjects/ASSD-TP2/src/SampleSynth/Guitar/'

    def play_note(self, noteFrequency, duration, fs, **kwargs):
        noteNumber = kwargs['noteNumber']
        note = None

        semitonalDiff = noteNumber - 60
        sample, sample_fs = sf.read(self.samplesPath + '60.wav')
        note = ssynth.averageChannels(sample)

        if semitonalDiff:
            note = ssynth.pitchShift(note, 1024, 256, semitonalDiff)

        sample_len = note.size / sample_fs
        timeFactor = duration / sample_len

        if timeFactor != 1:
            note = ssynth.timeScaler(note, 1024, 256, timeFactor)

        return note