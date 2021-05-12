import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from AdditiveSynthesizer import AddSynth

# ------------------------------------------------------------
if __name__ == '__main__':
    data, rate = sf.read('C:/Users/Philippe/PycharmProjects/ASSD-TP2/resources/Samples/flute-C4.wav')
    t = np.linspace(0, data.shape[0] / rate, data.shape[0])  # start stop num
    rocola = AddSynth()
    flute_harmonics = [1, 2, 3, 4, 5, 6, 7, 8, 9] #261.626
    flute_amplituds = [351.66, 510.63, 178.22, 67.94, 79.84, 27.96, 24.81, 29.51, 9.01]
    piano_harmonics = [1, 2, 3, 4, 6, 7, 8, 9]
    piano_amplituds = [356.88, 251.73, 31.64, 39.84, 38.67, 10.56, 15.06, 13.04]
    rocola.create_partials(705.9, flute_harmonics, flute_amplituds, data.shape[0] / rate, rate / 2)
    f_sound = rocola.apply_ADSR(2.438, 0.358, 0.358, 0.128, 3026, 2833, 2489, rate / 2) #dtA,dtD,dtS,dtR,kAo,Ao,So,fs
    x, sound = rocola.plot_me()
    plt.plot(x, f_sound)
    plt.plot(t, data)
    plt.show()
