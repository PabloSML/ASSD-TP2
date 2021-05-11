import numpy as np

def karplus_strong(wavetable, n_samples, stretch_factor = 1):
    """Synthesizes a new waveform from an existing wavetable, modifies last sample by averaging.
    Uses a stretch_factor to control for decay."""
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