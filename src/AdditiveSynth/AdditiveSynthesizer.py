import numpy as np
from partial import partial
from random import gauss
from math import ceil



class AddSynth:

    def __init__(self, parent=None):
        self.sound = None
        self.x = None

    def create_note(self, freq, duration, instrumento, fs=5500):

        nota = ('C7' if freq > 650 else 'C4') if instrumento != 'guitar' else 'C4'
        data = self.instrument_data(instrumento + nota)

        self.create_partials(freq, data[0], data[1], duration, fs)
        t_ADSR = np.array(data[2][:6]) * duration / 100.0
        params_ADSR = np.concatenate([t_ADSR,data[2][6:]])

        sound = self.ADSR(params_ADSR, fs)

        return self.x, sound

    def create_partials(self, freq, harmonics, amplituds, length, fs=4000):

        self.x = np.arange(0, length, 1 / fs)
        self.sound = np.zeros(self.x.size)

        for i in range(len(harmonics)):
            self.sound += amplituds[i] * np.sin(self.x * 2*np.pi*gauss(freq * harmonics[i], 2))

    def ADSR(self, t_ADSR, fs):

        s = self.apply_ADSR(t_ADSR[0], t_ADSR[1], t_ADSR[2], t_ADSR[3], t_ADSR[4], t_ADSR[5], t_ADSR[6], t_ADSR[7],
                            t_ADSR[8], fs)
        return s

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

        enveloped_sound = self.sound/max(abs(self.sound)) * ADSR
        return enveloped_sound

    def instrument_data(self, instrument):
        """
             Estructura del instrumento: wav, harmonicos, amplitudes, ADSR (dt [%], Amplitudes)
        """
        repertorio = {
            'pianoC4':[[1, 2, 3, 4, 5, 6, 7, 8, 9],  #Harmonicos
                       [0.01088, 0.00768, 0.000966, 0.001225, 0.00118, 0.00119, 0.000125, 0.000323, 0.000466],  # Amplitudes
                       [1.464, 1.212, 2.124, 27.38, 54.63, 13.19, 0.0517, 0.078, 0.02]],
             'fluteC4':[[1, 2, 3, 4, 5, 6, 7, 8], #Harmonicos
                        [0.01077, 0.01566, 0.00548, 0.002075, 0.00248, 0.00084, 0.00074, 0.0009], #Amplitudes
                        [2.5, 3.15, 68.35, 21.3, 3.3, 1.4, 0.055, 0.0931, 0.0775]],
            'trumpetC4':[[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], #Harmonicos
                       [0.00155, 0.002183, 0.003763, 0.00498, 0.00188, 0.00406, 0.00205, 0.001269, 0.001004, 0.00084, 0.0011, 0.00062], #Amplitudes
                       [5, 0.65, 5.24, 83.46, 1.93, 3.72, 0.052, 0.0923, 0.0467]],
            'violinC4':[[1, 2, 3, 4, 5, 6, 7, 8, 9], #Harmonicos
                       [0.031, 0.01204, 0.00748, 0.00427, 0.00495, 0.00304, 0.001503, 0.002072, 0.002408], #Amplitudes
                       [0.63, 21.37, 67.97, 4.29, 5.74, 0, 0.184, 0.16, 0.0258]],
            'pianoC6':[[1, 2], #Harmonicos
                       [0.01, 0.0024], #Amplitudes
                       [3.3, 1.7, 25, 60, 10, 0, 0.08, 0.02, 0.05]],
            'trumpetC6': [[1, 2, 3, 4],  # Harmonicos
                        [0.0217, 0.00258, 0.00123, 0.00024],  # Amplitudes
                        [12, 2.6, 28.9,49.5, 2.3, 4.7, 0.0715, 0.007, 0.0463]],
            'fluteC6': [[1, 2, 3, 4],  # Harmonicos
                        [0.025, 0.0002, 0.0007, 0.0005],  # Amplitudes
                        [0.7, 1, 14.7, 78.6, 3.7, 1.3, 0.0929, 0.0989, 0.1028]],
            'pianoC6': [[1, 2, 3, 4, 5],  # Harmonicos
                        [0.01557, 0.005015, 0.005403, 0.001, 0.0004],  # Amplitudes
                        [1.36, 16.569, 40.491, 35.58, 6, 0, 0.08145, 0.0561]],
            'guitarC4': [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],  # Harmonicos
                        [0.0329, 0.024, 0.012, 0.0324, 0.003, 0.0132, 0.005, 0.004, 0.0008, 0.002, 0.0023, 0.0024], # Amplitudes
                        [0, 0.229, 11.271, 48.5, 22, 18, 0.8615, 0.16, 0.0252]]}

        return repertorio[instrument]

    def plot_me(self):
        return (self.x, self.sound)

#------------------------------------------------------------------
if __name__ == '__main__':
    import matplotlib.ticker as ticker
    import matplotlib.pyplot as plt
    import soundfile as sf
    from scipy import signal
    from scipy.fft import fft, fftfreq

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


    instrumento = 'flute'
    f = 261
    data, rate = sf.read('../../resources/Samples/' + instrumento + '-C6.wav')
    if instrumento == 'guitar':
        data = data[:,0]
    h = 5
    # sos = signal.butter(10, [261.626*0.9*h,261.626*1.1*h], 'bandpass', fs=rate, output='sos')
    # data = signal.sosfilt(sos, data)

    fs = rate
    w = 2
    t = np.linspace(0, data.shape[0] / rate, data.shape[0])
    #adsr, upper, lower = compute_ADSR(data, w, fs)
    yf = fft(data)
    xf = fftfreq(data.shape[0], 1 / rate)[:data.shape[0] // 2]
    #print(max(2.0 / data.shape[0] * np.abs(yf[0:data.shape[0] // 2])))

    # ----- PLOT ----- #
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.subplots_adjust(hspace=0.3)
    #fig.suptitle(instrumento.upper())

    ax1.set_title(instrumento.upper())
    ax1.set_xlabel('tiempo [s]')
    ax1.plot(np.linspace(0,100, data.shape[0]), data)
    ax1.grid(True)

    ax2.plot(xf, 2.0 / data.shape[0] * np.abs(yf[0:data.shape[0] // 2]))
    ax2.set_xlabel('frecuencia [Hz]')
    ax2.set_xlim(0,f*13)
    ax2.xaxis.set_major_locator(ticker.MultipleLocator(f))
    ax2.xaxis.set_minor_locator(ticker.MultipleLocator(f/5))
    ax2.grid(True)

    #plt.grid()
    plt.show()