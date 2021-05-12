import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from AdditiveSynthesizer import AddSynth
from scipy.fft import fft, fftfreq
import matplotlib.ticker as ticker
# ------------------------------------------------------------
if __name__ == '__main__':

    instrumento = 'violin'

    original, rate = sf.read('../../resources/Samples/' + instrumento + '-C4.wav')
    t = np.linspace(0, original.shape[0] / rate, original.shape[0])  # start stop num

    rocola = AddSynth()
    x, monster = rocola.create_note(261.626, original.shape[0]/rate, instrumento, rate)

    of = fft(original)
    xf1 = fftfreq(original.shape[0], 1 / rate)[:original.shape[0] // 2]
    mf = fft(monster)
    xf2 = fftfreq(monster.shape[0], 1 / rate)[:monster.shape[0] // 2]

    fig, axs = plt.subplots(2, 2)
    axs[0,0].plot(x, monster)
    axs[0,1].plot(xf1, 2.0 / monster.shape[0] * np.abs(mf[0:monster.shape[0] // 2]))
    axs[0,1].xaxis.set_major_locator(ticker.MultipleLocator(261))
    axs[0,1].set_xlim(0, 261 * 10)

    axs[1,0].plot(t, original)
    axs[1,1].plot(xf2, 2.0 / original.shape[0] * np.abs(of[0:original.shape[0] // 2]))
    axs[1,1].xaxis.set_major_locator(ticker.MultipleLocator(261))
    axs[1,1].set_xlim(0, 261 * 10)
    plt.show()

    sf.write('piano_exp.wav', monster, rate)
