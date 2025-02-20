import numpy as np
import matplotlib.pyplot as plt

# Parametre
f_c = 10  # Bærerfrekvens (Hz)
sampling_rate = 1000  # Samplingrate (Hz)
T = 1 / f_c  # Periode
t = np.linspace(0, 2 * T, 1000)  # Tid for 2 perioder

# Faseforskyvning i grader
phase_shift_deg = 40  # 40 grader
phase_shift_rad = np.deg2rad(phase_shift_deg)  # Konverter til radianer

# Generer I og Q komponenter
I = np.cos(2 * np.pi * f_c * t)  # I-komponent (in-phase)
Q = np.sin(2 * np.pi * f_c * t)  # Q-komponent (quadrature)

# Lag den faseforskyvde sinusbølgen
sinus_wave = np.cos(2 * np.pi * f_c * t + phase_shift_rad)  # 40 grader faseforskyvning

# Plotting
plt.figure(figsize=(10, 6))

# Plot sinusfunksjonen med faseforskyvning
plt.subplot(3, 1, 1)
plt.plot(t, sinus_wave, label="Faseforskjøvet sinusbølge (40 grader)", color="r")
plt.title("Faseforskjøvet Sinusbølge (40 grader)")
plt.xlabel("Tid [s]")
plt.ylabel("Amplitud")
plt.grid(True)
plt.legend()

# Plot I-komponenten
plt.subplot(3, 1, 2)
plt.plot(t, I, label="I-komponent (In-phase)", color="b")
plt.title("I-komponent (In-phase)")
plt.xlabel("Tid [s]")
plt.ylabel("Amplitud")
plt.grid(True)
plt.legend()

# Plot Q-komponenten
plt.subplot(3, 1, 3)
plt.plot(t, Q, label="Q-komponent (Quadrature)", color="g")
plt.title("Q-komponent (Quadrature)")
plt.xlabel("Tid [s]")
plt.ylabel("Amplitud")
plt.grid(True)
plt.legend()

# Vis grafene
plt.tight_layout()
plt.show()
