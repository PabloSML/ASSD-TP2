import numpy as np

def karplus_strong(wavetable, n_samples, stretch_factor = 1):
    samples = []
    current_sample = 0
    previous_value = 0
    # while len(samples) < n_samples:
    #     wavetable[current_sample] = 0.5 * (wavetable[current_sample] + previous_value)
    #     samples.append(wavetable[current_sample])
    #     previous_value = samples[-1]
    #     current_sample += 1
    #     current_sample = current_sample % wavetable.size

    while len(samples) < n_samples:
        r = np.random.binomial(1, 1 - 1/stretch_factor)
        if r == 0:
            wavetable[current_sample] =  0.5 * (wavetable[current_sample] + previous_value)
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)

def karplus_strong_drum(wavetable, n_samples, b = 0.5):
    samples = []
    current_sample = 0
    previous_value = 0
    RL = 0.9995
    while len(samples) < n_samples:
        r = np.random.binomial(1, b)
        sign = float(r == 1) * 2 - 1
        wavetable[current_sample] = sign * 0.5 * RL * (wavetable[current_sample] + previous_value)
        samples.append(wavetable[current_sample])
        previous_value = samples[-1]
        current_sample += 1
        current_sample = current_sample % wavetable.size
    return np.array(samples)