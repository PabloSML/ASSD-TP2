from mido import MidiFile
import numpy as np
from src.Track import Track
from src.SamAsh import SamAsh
import soundfile as sf
import pyaudio
import time
# from src.Effects.Eco_simple import eco_simple_FX
# from src.Effects.Reverb_LP import LP_Reverb_FX
# from src.Effects.Flanger import Flanger_FX



class TurnTable:

    def __init__(self, midi_file=None):
        self.midi_file = midi_file
        self.trackList = []
        self.store = SamAsh()
        self.fs = 48000
        self.songLength = None
        self.song = None
        self.chunkSize = 1024
        self.chunkIndex = None
        self.paObj = None
        self.player = None


    def load(self, midi_path=None):
        self.midi_file = MidiFile(midi_path)
        current_tick = 0
        uspb_tempos = []  # uspb = micro-sec per beat
        spt_tempos = None  # spt = seconds per tick

        for msg in self.midi_file.tracks[0]:
            current_tick += msg.time
            if msg.is_meta and msg.type == 'set_tempo':
                uspb_tempos.append([current_tick, msg.tempo])
        uspb_tempos = np.array(uspb_tempos).T
        spt_tempos = np.array([uspb_tempos[0], uspb_tempos[1] / (1e6 * self.midi_file.ticks_per_beat)])
        self.songLength = int(np.ceil(self.fs * self.midi_file.length))
        self.song = np.zeros(self.songLength)

        tracksCreated = 0
        for index, track in enumerate(self.midi_file.tracks[1:]):
            lastEv = track[-2]  # Sin contar End-Of-Track
            if lastEv.type.find('note') != -1 or lastEv.type.find('control') != -1:  # Ver que la track sea de notas
                self.trackList.append(Track(midiLength=self.songLength, midiTrack=track, trackNumber=index+1,
                                            spt_tempos=spt_tempos, store=self.store, fs=self.fs))
                tracksCreated += 1
                # self.trackList[index].set_instrument('sampleGuitar')


    def set_fs(self, new_fs):
        self.fs = new_fs


    def synthesize(self):
        for track in self.trackList:
            # if track.isActive:
            track.synthesize_track()
        self.normalize_tracks()
        print('Synthesized all tracks')


    def process_chunk(self, in_data, frame_count, time_info, status):
        playbackData = np.zeros(self.chunkSize).astype(np.float32)

        for track in self.trackList:
            chunkAudio = track.audioTrack[self.chunkIndex*self.chunkSize: (self.chunkIndex+1)*self.chunkSize] * track.volume
            playbackData[:chunkAudio.size] += chunkAudio

        sound = self.prep_playback(playbackData)
        self.chunkIndex += 1
        if self.chunkIndex*self.chunkSize < self.song.size:
            return (sound, pyaudio.paContinue)
        else:
            self.chunkIndex = None
            return (sound, pyaudio.paComplete)


    def start_playback(self):

        if self.chunkIndex is None:
            self.chunkIndex = 0
        # instancio PyAudio
        if self.paObj is None:
            self.paObj = pyaudio.PyAudio()
        # abrimos player
        if self.player is None:
            self.player = self.paObj.open(rate=self.fs, channels=1, output=True, format=pyaudio.paFloat32, stream_callback=self.process_chunk)

        if not self.player.is_active():
            self.player.start_stream()


    def pause_playback(self):
        if self.player.is_active():
            self.player.stop_stream()


    def stop_playback(self):
        if self.player is not None:
            if self.player.is_active():
                self.player.stop_stream()
            self.player.close()
            self.player = None
        if self.paObj is not None:
            self.paObj.terminate()
            self.paObj = None
        self.chunkIndex = None


    def prep_playback(self, data):

        maxAmp = np.abs(data).max()
        if maxAmp > 1:
            data = data / maxAmp

        return (data.astype(np.float32)).tobytes()


    def normalize_tracks(self):
        maxLenTrack = self.songLength
        for track in self.trackList:
            track.audioTrack = track.audioTrack / (np.abs(track.audioTrack)).max()
            if maxLenTrack < track.audioTrack.size:
                maxLenTrack += track.audioTrack.size - maxLenTrack
            elif maxLenTrack > track.audioTrack.size:
                track.audioTrack = np.append(track.audioTrack, np.zeros(maxLenTrack - track.audioTrack.size))

        if maxLenTrack > self.songLength:
            self.song = np.append(self.song, np.zeros(maxLenTrack - self.songLength))


    def master(self, masterPath = 'D:/PycharmProjects/ASSD-TP2/tests/', masterName = 'Master', masterFormat = '.wav'):
        for track in self.trackList:
            if track.isActive:
                self.song += track.audioTrack * track.volume

        sf.write(masterPath + masterName + masterFormat, self.song, self.fs)


# Test Bench

beogram4000C = TurnTable()
beogram4000C.load('D:/PycharmProjects/ASSD-TP2/tests/rodriG.mid')
beogram4000C.synthesize()

# # Playback Test
beogram4000C.start_playback()
while beogram4000C.player.is_active():
    time.sleep(0.1)
beogram4000C.stop_playback()

# Mastering Test
# beogram4000C.master()
