import numpy as np

# Generer et tilfeldig signal
fs = 1000  # Samplingsfrekvens (Hz)
t = np.linspace(0, 1, fs, endpoint=False)  # Tidsakse
signal = np.sin(t*2*np.pi) + np.cos (t*2*np.pi)  # Tilfeldig signal

# Bærebølgen
carrier_freq = 50  # Bærebølgefrekvens (Hz)
I_carrier = np.cos(2 * np.pi *  t)  # In-phase bærebølge
Q_carrier = np.sin(2 * np.pi *  t)  # Quadrature bærebølge

# Demoduler for å finne I og Q
I = signal * I_carrier  # I-komponenten
Q = signal * Q_carrier  # Q-komponenten

# Kombiner I og Q til ett datasett
IQ_data = np.column_stack((I, Q)).astype(np.float32)  # 32-bit floats

# Lagre til en .bin-fil
filename = "iq_data_no_filter.bin"
IQ_data.tofile(filename)

print(f"I/Q-data lagret til {filename}")