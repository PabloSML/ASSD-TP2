import numpy as np
import soundfile as sf

# El eco simple se puede modelar con la ecuacion en diferencias
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
    output_sample[no_change:] = input_sample[no_change:]+gain*input_sample[:len(input_sample)-no_change]
    return output_sample

#######################################
#Faltaria implementar lo mismo con FFT#
#######################################


if __name__ == "__main__":
    audio, fs = sf.read('/tests/promo_m.wav')
    #leftChannel = audio[:, 0]
    out = eco_simple_FX(audio,delay=100,sample_rate=fs)
    sf.write('test_effects/promo_eco.wav', out, fs)

