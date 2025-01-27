import numpy as np
import matplotlib.pyplot as plt

# Filnavnet til binærfilen
filename = "iq_data_no_filter.bin"  # Bytt til filen din

# Les inn I/Q-data fra filen
IQ_data = np.fromfile(filename, dtype=np.float32)

# Split dataen i I- og Q-komponenter
I = IQ_data[::2]  # Hent I-komponenten (annenhver verdi)
Q = IQ_data[1::2]  # Hent Q-komponenten (annenhver verdi)

# Parametere for signalrekonstruksjon
fs = 1000  # Samplingsfrekvens (Hz), sett denne til det du brukte
 # Bærebølgefrekvens (Hz), må samsvare med det opprinnelige signalet
t = np.arange(len(I))/fs   # Tidsakse

# Rekonstruer det originale signalet
reconstructed_signal = I * np.cos(2 * np.pi *   t) + Q * np.sin(2 * np.pi *  t)

# Plot det rekonstruerte signalet
plt.figure(figsize=(10, 4))
plt.plot(t, reconstructed_signal, label="Rekonstruert signal", color='b')
plt.title("Rekonstruert signal")
plt.xlabel("Tid (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
