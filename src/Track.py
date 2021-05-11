import numpy as np
from mido import MidiFile
from src.SamAsh import SamAsh
from src.Instrument import Instrument
from src.SampleSynth import SampleSynth


class Track:
    def __init__(self, midiLength=None, midiTrack = None, trackNumber=None, spt_tempos=None,
                 store: SamAsh=None, noteNumDecoder=None, fs=None):
        self.midiLength = midiLength
        self.midiTrack = midiTrack
        self.trackNumber = trackNumber
        self.fs = fs
        self.spt_tempos = spt_tempos
        self.audioTrack = None
        self.isActive = False
        self.store = store
        self.noteNumDecoder = noteNumDecoder
        self.instrument = None
        self.instrumentName = None
        self.funNoteFreqs = {'A': 27.5, 'A#': 29.0, 'B': 30.87, 'Bb': 29.135, 'C': 16.35, 'C#': 17.32, 'D': 18.35,
                             'D#': 19.0, 'E': 20.6, 'Eb': 19.445, 'F': 21.83, 'F#': 23.12, 'G': 24.5, 'G#': 25.96}

    def toggle_active(self):
        self.isActive = not self.isActive

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

            if not ev.is_meta and ev.type == 'note_on':
                noteData = self.noteNumDecoder.loc[ev.note]
                noteFunFreq = self.funNoteFreqs[noteData['Note']]
                octave = noteData['Octave']
                noteFrequency = noteFunFreq * 2**octave
                tickDuration, velocity = self.find_note_off(ev.note, ev.channel, index)
                realDuration = tickDuration * spt_tempo

                noteAudio = self.instrument.play_note(frequency=noteFrequency, duration=realDuration)

                if np.count_nonzero(noteAudio) != 0:    # si la nota efectivamente se genero
                    noteAudio *= max(velocity, ev.velocity) / np.abs(noteAudio).max() * octave  # normaliza la velocidad
                    noteBeg = int(np.round(self.fs * realTime))
                    if noteBeg + noteAudio.size > self.audioTrack.size:
                        self.audioTrack = np.append(self.audioTrack, np.zeros(noteBeg + noteAudio.size - self.audioTrack.size))
                    self.audioTrack[noteBeg:noteBeg+noteAudio.size] += noteAudio

    def find_note_off(self, noteNumber, channel, currentIndex):
        tickDelta = 0

        for futureEv in self.midiTrack[currentIndex+1:]:
            tickDelta += futureEv.time
            if (not futureEv.is_meta) and (futureEv.note == noteNumber) and (futureEv.channel == channel):
                if futureEv.type == 'note_off':
                    return tickDelta, futureEv.velocity
                elif futureEv.type == 'note_on':
                    futureEv.type = 'note_off'
                    return tickDelta, futureEv.velocity

        return None, None
