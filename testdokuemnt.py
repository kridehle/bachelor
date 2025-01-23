import numpy as np
import matplotlib.pyplot as plt

def barker_code(n):
    """
    Generate the Barker code for a given length n.
    Barker codes exist only for specific lengths: 2, 3, 4, 5, 7, 11, 13.
    """
    barker_sequences = {
        2: [1, -1],
        3: [1, 1, -1],
        4: [1, 1, -1, 1],
        5: [1, 1, 1, -1, 1],
        7: [1, 1, 1, -1, -1, 1, -1],
        11: [1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1],
        13: [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    }
    
    if n not in barker_sequences:
        raise ValueError(f"Barker code of length {n} does not exist.")
    
    return barker_sequences[n]

# Parameters
n = 7  # Length of Barker code
barker_seq = barker_code(n)
bit_duration = 0.1  # Duration of each Barker code bit (seconds)
fs = 1000  # Sampling frequency (samples per second)

# Create the NRZ waveform
samples_per_bit = int(fs * bit_duration)
nrz_waveform = np.repeat(barker_seq, samples_per_bit)

# Create the time vector for the NRZ waveform
total_duration = len(barker_seq) * bit_duration
t = np.linspace(0, total_duration, len(nrz_waveform), endpoint=False)

# Plot the NRZ waveform
plt.figure(figsize=(10, 4))
plt.plot(t, nrz_waveform, drawstyle="steps-pre", label="NRZ Barker Code")
plt.title(f"NRZ Encoding of Barker Code (Length {n})")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.ylim(-1.5, 1.5)
plt.grid()
plt.legend()
plt.show()
