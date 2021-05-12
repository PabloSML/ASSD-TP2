import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

# y(n) = x(n) - g (y(n-M) + y(n-M-1))

# Reverb_LP_FX
# Que recibe:
#       -Audio,longitud indeterminada (de esto depende la velocidad de procesamiento)
#       -Ganancia del eco (<1)
#       -delay del eco (en ms)
#       -fs de la señal de audio
# Que devuelve:
#       -Audio de misma longitud con efecto aplicado
def LP_Reverb_FX(input_sample, gain=0.3 , delay=20, sample_rate=44100):
    output_sample = np.zeros_like(input_sample)
    no_change = int(np.floor(delay * sample_rate / 1000))
    output_sample[:no_change] = input_sample[:no_change]  # hasta M y(n)=x(n)
    output_sample[no_change] = input_sample[no_change] - gain * output_sample[0]  # en M es y(n)=x(n)-gain*(Y(n-M))
    for it in range(no_change + 1, len(input_sample)):
        output_sample[it] = input_sample[it] - gain * (output_sample[it - no_change] + output_sample[
            it - no_change - 1])  # es y(n)=x(n)-gain*(Y(n-M)+Y(n-M-1))
    return output_sample


if __name__ == "__main__":
    audio, fs = sf.read('C:/Users/FranciscoDanielLedes/PycharmProjects/ASSD-TP2/tests/hola.wav')
    # leftChannel = audio[:, 0]
    out = LP_Reverb_FX(audio, delay=10, sample_rate=fs)

    time = np.linspace(0,5,len(audio))
    fig, axs = plt.subplots(2)
    fig.suptitle('Reverberador pasa-bajos')
    axs[0].plot(time, audio)
    axs[0].set(ylabel='input')
    axs[1].plot(time, out)
    axs[1].set(xlabel='time(s)',ylabel='output')
    plt.show()

    sf.write('test_effects/hola_LP_reverb.wav', out, fs)
