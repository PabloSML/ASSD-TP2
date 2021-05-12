import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

# Y(n) = x(n) + g.x(n-M(n))
# M(n) = delay(1+sen(2.pi.n.f0/fs))
# Flanger_FX
# Que recibe:
#       -Audio,longitud indeterminada (de esto depende la velocidad de procesamiento)
#       -Ganancia del eco (<1)
#       -delay del eco (en ms)
#       -f0
#       -fs de la señal de audio
# Que devuelve:
#       -Audio de misma longitud con efecto aplicado
def Flanger_FX(input_sample, gain=5 / 3, delay=20, sample_rate=44100, f0=1.2):
    output_sample = np.zeros_like(input_sample)
    no_change = int(np.floor(delay * sample_rate / 1000))
    output_sample[:no_change + 2] = input_sample[:no_change + 2]

    # first try con for
    for it in range(no_change, len(input_sample)):
        M = int(np.floor(no_change * (1 + np.sin(2 * np.pi * it * f0 / sample_rate))))
        output_sample[it] = input_sample[it] + gain * input_sample[it - M]
    return output_sample


if __name__ == "__main__":
    audio, fs = sf.read('C:/Users/FranciscoDanielLedes/PycharmProjects/ASSD-TP2/tests/hola.wav')
    # leftChannel = audio[:, 0]
    out = Flanger_FX(audio, delay=10, sample_rate=fs)

    time = np.linspace(0, 5, len(audio))
    fig, axs = plt.subplots(2)
    fig.suptitle('Flanger')
    axs[0].plot(time, audio)
    axs[0].set(ylabel='input')
    axs[1].plot(time, out)
    axs[1].set(xlabel='time(s)', ylabel='output')
    plt.show()

    sf.write('test_effects/hola_flanger.wav', out, fs)
