import numpy as np
import soundfile as sf

# La reverberacion se puede modelar con la ecuacion en diferencias
# """ y(n) = x(n) - g (y(n-M) + y(n-M-1))  """

# Reverb_LP_FX
# Que recibe:
#       -Audio,longitud indeterminada (de esto depende la velocidad de procesamiento)
#       -Ganancia del eco (<1)
#       -delay del eco (en ms) minimo 100ms para ser apreciable?
#       -fs de la senial de audio
# Que devuelve:
#       -Audio de misma longitud con efecto aplicado
def LP_Reverb_FX(input_sample, gain=0.7/5, delay=20, sample_rate=44100):
    output_sample = np.zeros_like(input_sample)
    no_change = int(np.floor(delay * sample_rate / 1000))
    output_sample[:no_change] = input_sample[:no_change]                            #hasta M y(n)=x(n)
    output_sample[no_change] = input_sample[no_change] - gain*output_sample[0]       #en M es y(n)=x(n)-gain*(Y(n-M))
    for it in range(no_change+1,len(input_sample)):
        output_sample[it]=input_sample[it]-gain*(output_sample[it-no_change]+output_sample[it-no_change-1]) #es y(n)=x(n)-gain*(Y(n-M)+Y(n-M-1))

   # output_sample[no_change+1:] = input_sample[no_change+1:] - gain*(output_sample[1:len(output_sample)-no_change-1]+output_sample[0:len(output_sample)-no_change])

    return output_sample

#######################################
#Faltaria implementar lo mismo con FFT#
#######################################


if __name__ == "__main__":
    audio, fs = sf.read('/tests/promo_m.wav')
    #leftChannel = audio[:, 0]
    out = LP_Reverb_FX(audio,delay=500,sample_rate=fs)
    sf.write('test_effects/promo_LP_reverb.wav', out, fs)
