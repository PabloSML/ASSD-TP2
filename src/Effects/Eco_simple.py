import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Y(n) = x(n) + g.X(n-m)

# Eco_simple_FX
# Que recibe:
#       -Audio,longitud indeterminada (de esto depende la velocidad de procesamiento)
#       -Ganancia del eco (<1)
#       -delay del eco (en ms) minimo 100ms para ser apreciable?
#       -fs de la senial de audio
# Que devuelve:
#       -Audio de misma longitud con efecto aplicado
def eco_simple_FX(input_sample, gain=0.5, delay=20, sample_rate=44100):
    output_sample = np.zeros_like(input_sample)
    no_change = int(np.floor(delay * sample_rate / 1000))
    output_sample[:no_change] = input_sample[:no_change]
    output_sample[no_change:] = input_sample[no_change:] + gain * input_sample[:len(input_sample) - no_change]
    return output_sample


if __name__ == "__main__":
    audio, fs = sf.read('C:/Users/FranciscoDanielLedes/PycharmProjects/ASSD-TP2/tests/hola.wav')
    # leftChannel = audio[:, 0]
    out = eco_simple_FX(audio, delay=500, sample_rate=fs)

    time = np.linspace(0,5,len(audio))
    fig, axs = plt.subplots(2)
    fig.suptitle('Eco simple')
    axs[0].plot(time, audio)
    axs[0].set(ylabel='input')
    axs[1].plot(time, out)
    axs[1].set(xlabel='time(s)',ylabel='output')
    plt.show()

    sf.write('test_effects/hola_eco.wav', out, fs)
