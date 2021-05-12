import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from partial import partial
from random import gauss
from math import ceil
from scipy.fft import fft, fftfreq


class AddSynth:

    def __init__(self, parent=None):
        self.sound = None
        self.x = None

    def create_note(self, freq, duration, instrumento, fs=5500):

        nota = 'C7' if freq > 650 else 'C4'
        data = self.instrument_data(instrumento + nota)
        self.create_partials(freq, data[1], data[2], duration, fs)
        t_ADSR = np.array(data[3]) * duration / 100.0
        sound = self.apply_ADSR(t_ADSR[0], t_ADSR[1], t_ADSR[2], t_ADSR[3], t_ADSR[4], t_ADSR[5], t_ADSR[6], t_ADSR[7], t_ADSR[8], fs)
        return self.x, sound

    def create_partials(self, freq, harmonics, amplituds, length, fs=4000):
        self.x = np.arange(0, length, 1 / fs)
        self.sound = np.zeros(self.x.size)
        for i in range(len(harmonics)):
            self.sound += amplituds[i] * np.sin(self.x * gauss(freq * harmonics[i], 1))

    def apply_ADSR(self, dti, dtA, dtD, dtS, dtR, dtf, kAo, Ao, So, fs):
        inicio = np.zeros(int(dti * fs))
        stageA = np.arange(0, dtA, 1 / fs) * kAo / dtA
        stageD = np.arange(0, dtD, 1 / fs) * ((Ao - kAo) / dtD) + kAo
        stageS = np.arange(0, dtS, 1 / fs) * ((So - Ao) / dtS) + Ao
        stageR = np.arange(0, dtR, 1 / fs) * (-So / dtR) + So
        final = np.zeros(int(dtf * fs))
        ADSR = np.concatenate([inicio, stageA, stageD, stageS, stageR, final], axis=None)
        if len(self.sound) > len(ADSR):
            ADSR = np.concatenate([ADSR, np.zeros(len(self.sound) - len(ADSR))])
        else:
            if len(self.sound) < len(ADSR):
                ADSR = ADSR[:len(self.sound)]
            enveloped_sound = self.sound / max(self.sound) * ADSR
            return enveloped_sound

    def instrument_data(self, instrument):
        """
             Estructura del instrumento: wav, harmonicos, amplitudes, ADSR (dt [%], Amplitudes)
        """
        repertorio = {
            'pianoC4':['../resources/Samples/piano-C4.wav', [1, 2, 3, 4, 6, 7, 8, 9],[356.88, 251.73, 31.64, 39.84, 38.67, 10.56, 15.06, 13.04],[0.068, 0.1293, 0.717, 2.698, 2493, 2544, 930]],
            'fluteC4':['../resources/Samples/flute-C4.wav', [1, 2, 3, 4, 5, 6, 7, 8, 9],[351.66, 510.63, 178.22, 67.94, 79.84, 27.96, 24.81, 29.51, 9.01],[2.44, 0.36, 0.358, 0.128, 3026, 2833, 2489]],
            'trumpetC4':['../resources/Samples/trumpet-C4.wav', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],[50.5, 70.7, 122.8, 162, 60.9, 133.6, 66.7, 40.8, 32.3, 28, 36.1],[5, 0.65, 5.24, 83.46, 1.93, 3.72, 1810, 3000, 1540]]}

        return repertorio[instrument]

    def plot_me(self):
        return (self.x, self.sound)

#------------------------------------------------------------------
if __name__ == '__main__':

    def compute_ADSR(signal, w_len=0.01, fs=4000):
        win_len_half = round(w_len * fs * 0.5)
        N = signal.shape[0]
        adsr = np.zeros(N)
        upper = np.zeros(N)
        lower = np.zeros(N)
        for i in range(N):
            start = max(0, i - win_len_half)
            end = min(N, i + win_len_half)
            adsr[i] = np.amax(np.abs(signal)[start:end])
            upper[i] = np.amax(signal[start:end])
            lower[i] = np.amin(signal[start:end])
        else:
            return (
             adsr, upper, lower)


    data, rate = sf.read('../resources/Samples/piano-C4.wav')
    fs = rate / 5
    w = 2
    t = np.linspace(0, data.shape[0] / rate, data.shape[0])
    adsr, upper, lower = compute_ADSR(data, w, fs)
    yf = fft(data)
    xf = fftfreq(data.shape[0], 1 / rate)[:data.shape[0] // 2]
    print(max(2.0 / data.shape[0] * np.abs(yf[0:data.shape[0] // 2])))
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.set_title('trumpet')
    ax1.plot(np.linspace(0, 100, data.shape[0]), data)
    ax2.plot(xf, 2.0 / data.shape[0] * np.abs(yf[0:data.shape[0] // 2]))
    plt.grid()
    plt.show()