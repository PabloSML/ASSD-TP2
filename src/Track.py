import numpy as np
# from mido import MidiFile
from src.SamAsh import SamAsh
# from src.Instrument import Instrument
# from src.SampleSynth import sample_synth


class Track:
    def __init__(self, midiLength=None, midiTrack = None, trackNumber=None, spt_tempos=None,
                 store: SamAsh=None, fs=None):
        self.midiLength = midiLength
        self.midiTrack = midiTrack
        self.usedNoteOff = []
        self.trackNumber = trackNumber
        self.fs = fs
        self.spt_tempos = spt_tempos
        self.audioTrack = None
        self.isActive = True
        self.volume = 1
        self.store = store
        self.instrument = None
        self.instrumentName = None
        self.funNoteFreqs = [16.35, 17.32, 18.35, 19.0, 20.6, 21.83, 23.12, 24.5, 25.96, 27.5, 29.0, 30.87]
        # self.funNoteFreqs = {'A': 27.5, 'A#': 29.0, 'B': 30.87, 'C': 16.35, 'C#': 17.32, 'D': 18.35,
        #                      'D#': 19.0, 'E': 20.6, 'F': 21.83, 'F#': 23.12, 'G': 24.5, 'G#': 25.96}

    def toggle_active(self):
        self.isActive = not self.isActive

    def set_volume(self, newVolume):
        if newVolume >= 0.0 and newVolume <= 1.0:
            self.volume = newVolume

    def set_instrument(self, instrument_name):
        self.instrumentName = instrument_name
        self.instrument = self.store.loan_instrument(instrument_name)

    def current_spt_tempo(self, current_tick):
        return self.spt_tempos[1][self.spt_tempos[0].searchsorted(current_tick) - 1]

    def synthesize_track(self):
        print('Synthesizing track ' + str(self.trackNumber) + ' with ' + self.instrumentName)

        if self.audioTrack is None:
            self.audioTrack = np.zeros(self.midiLength)
        else:
            self.audioTrack = np.zeros_like(self.audioTrack[: self.midiLength])

        tickTime = realTime = 0

        for index, ev in enumerate(self.midiTrack):
            spt_tempo = self.current_spt_tempo(tickTime)
            realTime += ev.time * spt_tempo
            tickTime += ev.time

            if not ev.is_meta and ev.type == 'note_on' and not (index in self.usedNoteOff):
                fundamentalIndex = ev.note % 12
                noteFrequency = np.round(440 * 2**((ev.note - 69)/12), 2)    # Conversion numNota a frec
                octave = int(np.round(np.log2(noteFrequency/self.funNoteFreqs[fundamentalIndex])))
                tickDuration, velocity = self.find_note_off(ev.note, ev.channel, index)
                realDuration = tickDuration * spt_tempo * 1.5
                if realDuration > 8: realDuration = 2

                if self.instrumentName.find('sample') != -1:
                    noteAudio = self.instrument.play_note(noteFrequency=noteFrequency, duration=realDuration,
                                                          fs=self.fs, noteNumber=ev.note)
                else:
                    noteAudio = self.instrument.play_note(noteFrequency=noteFrequency, duration=realDuration,
                                                          fs=self.fs)

                if np.count_nonzero(noteAudio) != 0:    # si la nota efectivamente se genero
                    noteBeg = int(np.round(self.fs * realTime))
                    if noteBeg + noteAudio.size > self.audioTrack.size:
                        self.audioTrack = np.append(self.audioTrack, np.zeros(noteBeg + noteAudio.size - self.audioTrack.size))
                    self.audioTrack[noteBeg:noteBeg+noteAudio.size] += noteAudio

    def find_note_off(self, noteNumber, channel, currentIndex):
        tickDelta = 0

        for futureIndex, futureEv in enumerate(self.midiTrack[currentIndex+1:]):
            tickDelta += futureEv.time
            if (not futureEv.is_meta) and (futureEv.type.find('note') != -1) and (futureEv.note == noteNumber) \
                    and (futureEv.channel == channel):
                if futureEv.type == 'note_off':
                    return tickDelta, futureEv.velocity
                elif futureEv.type == 'note_on':
                    self.usedNoteOff.append(currentIndex+1 + futureIndex)
                    return tickDelta, futureEv.velocity

        return tickDelta, 0
