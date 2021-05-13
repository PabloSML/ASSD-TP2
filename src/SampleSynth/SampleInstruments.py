import numpy as np

from src.Instrument import Instrument
import src.SampleSynth.sample_synth as ssynth
import soundfile as sf


class SampleViolin(Instrument):
    def __init__(self):
        super(SampleViolin, self).__init__()
        self.samplesPath = 'D:/PycharmProjects/ASSD-TP2/src/SampleSynth/Violin/'

    def play_note(self, noteFrequency, duration, fs, **kwargs):
        noteNumber = kwargs['noteNumber']
        note = None

        if duration < 3:
            prefix = 'Violin_'
        else:
            prefix = 'ViolinLong_'

        if noteNumber in range(55, 109, 1):
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(noteNumber) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = middleChannel

        elif noteNumber < 55:
            semitonalDiff = noteNumber - 55
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(55) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = ssynth.pitchShift(middleChannel, 1024, 256, semitonalDiff)

        else:
            semitonalDiff = noteNumber - 108
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(108) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = ssynth.pitchShift(middleChannel, 1024, 256, semitonalDiff)

        sample_len = note.size/sample_fs
        timeFactor = duration/sample_len

        if np.abs(1 - timeFactor)*100 > 50:
            note = ssynth.timeScaler(note, 1024, 256, timeFactor)

        return note

class SamplePiano(Instrument):
    def __init__(self):
        super(SamplePiano, self).__init__()
        self.samplesPath = 'D:/PycharmProjects/ASSD-TP2/src/SampleSynth/Piano/'
        self.availableSamples = np.arange(27, 103, 3)

    def play_note(self, noteFrequency, duration, fs, **kwargs):
        noteNumber = kwargs['noteNumber']
        note = None
        duration *= 2

        if duration < 3:
            prefix = 'Piano_'
        else:
            prefix = 'PianoLong_'

        # Si la nota ya se encuentra sampleada
        if noteNumber in self.availableSamples:
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(noteNumber) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = middleChannel

        # Si la nota es más grave que D#1
        elif noteNumber < 27:
            semitonalDiff = noteNumber - 27
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(27) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = ssynth.pitchShift(middleChannel, 1024, 256, semitonalDiff)

        # Si la nota es más aguda que C8
        elif noteNumber > 102:
            semitonalDiff = noteNumber - 102
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(102) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = ssynth.pitchShift(middleChannel, 1024, 256, semitonalDiff)

        # Si la nota se encuentra entre samples
        else:
            notePos = np.searchsorted(self.availableSamples, noteNumber)
            noteToRight = self.availableSamples[notePos]
            noteToLeft = self.availableSamples[notePos-1]

            # Si la nota está más cerca de la menor de sus adyacentes
            if noteToRight - noteNumber == 2:
                sample, sample_fs = sf.read(self.samplesPath + prefix + str(noteToLeft) + '.wav')
                middleChannel = ssynth.averageChannels(sample)
                note = ssynth.pitchShift(middleChannel, 1024, 256, 1)

            # Si la nota está más cerca de la mayor de sus adyacentes
            else:
                sample, sample_fs = sf.read(self.samplesPath + prefix + str(noteToRight) + '.wav')
                middleChannel = ssynth.averageChannels(sample)
                note = ssynth.pitchShift(middleChannel, 1024, 256, -1)

        sample_len = note.size/sample_fs
        timeFactor = duration/sample_len

        if np.abs(1 - timeFactor)*100 > 50:
            note = ssynth.timeScaler(note, 1024, 256, timeFactor)

        return note

class SampleGuitar(Instrument):
    def __init__(self):
        super(SampleGuitar, self).__init__()
        self.samplesPath = 'D:/PycharmProjects/ASSD-TP2/src/SampleSynth/Sam/'
        self.availableSamples = np.arange(40, 77, 3)

    def play_note(self, noteFrequency, duration, fs, **kwargs):
        noteNumber = kwargs['noteNumber']
        note = None
        duration = max(2, duration*2)

        if duration < 3:
            prefix = 'Sam_'
        else:
            prefix = 'SamLong_'

        # Si la nota ya se encuentra sampleada
        if noteNumber in self.availableSamples:
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(noteNumber) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = middleChannel

        # Si la nota es más grave que E2
        elif noteNumber < 40:
            semitonalDiff = noteNumber - 40
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(40) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = ssynth.pitchShift(middleChannel, 1024, 256, semitonalDiff)

        # Si la nota es más aguda que E5
        elif noteNumber > 76:
            semitonalDiff = noteNumber - 76
            sample, sample_fs = sf.read(self.samplesPath + prefix + str(76) + '.wav')
            middleChannel = ssynth.averageChannels(sample)
            note = ssynth.pitchShift(middleChannel, 1024, 256, semitonalDiff)

        # Si la nota se encuentra entre samples
        else:
            notePos = np.searchsorted(self.availableSamples, noteNumber)
            noteToRight = self.availableSamples[notePos]
            noteToLeft = self.availableSamples[notePos-1]

            # Si la nota está más cerca de la menor de sus adyacentes
            if noteToRight - noteNumber == 2:
                sample, sample_fs = sf.read(self.samplesPath + prefix + str(noteToLeft) + '.wav')
                middleChannel = ssynth.averageChannels(sample)
                note = ssynth.pitchShift(middleChannel, 1024, 256, 1)

            # Si la nota está más cerca de la mayor de sus adyacentes
            else:
                sample, sample_fs = sf.read(self.samplesPath + prefix + str(noteToRight) + '.wav')
                middleChannel = ssynth.averageChannels(sample)
                note = ssynth.pitchShift(middleChannel, 1024, 256, -1)

        sample_len = note.size/sample_fs
        timeFactor = duration/sample_len

        if np.abs(1 - timeFactor)*100 > 50:
            note = ssynth.timeScaler(note, 1024, 256, timeFactor)

        return note
