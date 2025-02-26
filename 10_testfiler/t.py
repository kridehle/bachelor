import numpy as np
import matplotlib.pyplot as plt

# Parametere
fs = 1000  # Samplingsfrekvens (Hz)
f = 10  # Signalets frekvens (Hz)
T = 1  # Varighet i sekunder
t = np.linspace(0, T, fs * T, endpoint=False)  # Tidsvektor

# Generer sinusformet signal (kompleks representasjon)
signal = np.exp(1j * 2 * np.pi * f * t)  # e^(jωt)

# Ekstraher In-phase (I) og Quadrature (Q) komponentene
I = np.real(signal)  # In-phase (Reell del)
Q = np.imag(signal)  # Quadrature (Imaginær del)

# Plotting av signalene
plt.figure(figsize=(10, 6))

# Plot originalt signal (absoluttverdi for sammenligning)
plt.subplot(3, 1, 1)
plt.plot(t, np.abs(signal), label="Originalt signal (Amplitude)")
plt.legend()
plt.grid()

# Plot In-phase signal
plt.subplot(3, 1, 2)
plt.plot(t, I, label="In-phase (Reell del)", color="r")
plt.legend()
plt.grid()

# Plot Quadrature signal
plt.subplot(3, 1, 3)
plt.plot(t, Q, label="Quadrature (Imaginær del)", color="b")
plt.legend()
plt.grid()

plt.xlabel("Tid (s)")
plt.suptitle("IQ-signaldekomponering av en sinusbølge")
plt.tight_layout()
plt.show()
