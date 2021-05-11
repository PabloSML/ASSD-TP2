import numpy as np
from scipy.io import wavfile as wav
import matplotlib.pyplot as plt
from AdditiveSynthesizer import AddSynth


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
    return adsr, upper, lower
# ------------------------------------------------------------
if __name__ == '__main__':
    # '''
    #     Estructura del instrumento: wav, harmonicos, amplitudes, ADSR (dt [%], Amplitudes)
    # '''
    # repertorio = {'pianoC4':['../resources/Samples/piano-C4.wav', [1, 2, 3, 4, 6, 7, 8, 9], [356.88, 251.73, 31.64, 39.84, 38.67, 10.56, 15.06, 13.04], [0.068, 0.1293, 0.717, 2.698, 2493, 2544, 930]],
    #               'fluteC4':['../resources/Samples/flute-C4.wav', [1, 2, 3, 4, 5, 6, 7, 8, 9], [351.66, 510.63, 178.22, 67.94, 79.84, 27.96, 24.81, 29.51, 9.01], [2.440, 0.360, 0.358, 0.128, 3026, 2833, 2489]],
    #               'trumpetC4':['../resources/Samples/trumpet-C4.wav', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [50.5, 70.7, 122.8, 162, 60.9, 133.6, 66.7, 40.8, 32.3, 28, 36.1], [5, 0.65, 5.24, 83.46, 1.93, 3.72, 1810, 3000, 1540]]}
    #
    # instrumento = 'trumpetC4'
    # rate, data = wav.read(repertorio[instrumento][0])
    # t = np.linspace(0, data.shape[0] / rate, data.shape[0])  # start stop num
    # fs = rate
    # rocola = AddSynth()
    # env, upper, lower = compute_ADSR(data, 0.1, fs)
    # rocola.create_partials(261.626, repertorio[instrumento][1], repertorio[instrumento][2], data.shape[0] / rate, fs) #freq, harmonics, amplituds, length, fs
    # adsr = np.array(repertorio[instrumento][3]) * (data.shape[0]/rate) / 100.0
    # f_sound = rocola.apply_ADSR(adsr[0], adsr[1], adsr[2], adsr[3], adsr[4], adsr[5], adsr[6], adsr[7], adsr[8], fs) #dti,dtA,dtD,dtS,dtR,dtf,kAo,Ao,So,fs
    # x, sound = rocola.plot_me()
    # fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
    # ax1.set_title('original')
    # ax1.plot(t, data)
    # ax1.plot(t, env)
    # ax2.set_title('ADSR')
    # ax2.plot(x, f_sound)
    # ax3.set_title('invento')
    # ax3.plot(t, upper * sound / max(sound))
    # plt.show()
    #
    # wav.write(instrumento + '.wav', int(fs), f_sound)
    #
    test = AddSynth()
    x, y = test.create_note(261.626, 3, 'trumpet', 55100)
    plt.plot(x, y)
    plt.show()
