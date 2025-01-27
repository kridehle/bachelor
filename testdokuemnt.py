import numpy as np
import matplotlib.pyplot as plt

# Parametere for firkantpulsen
fs = 20000  # Samplingsfrekvens (Hz)
f = 5      # Firkantpulsens frekvens (Hz)
dc = 0.2   # Duty cycle (andel tid signalet er "på")
T = 1      # Total varighet (sekunder)
jitter_percent = 0.2  # Jitter som prosentandel av perioden (10%)

# Beregn perioden og pulsbredden
periode = 1 / f
puls_bredde = dc * periode

# Generer tidsvektor
t = np.linspace(0, T, int(fs * T), endpoint=False)

# Start- og sluttidspunkter for hver puls med jitter
start_tider = np.arange(0, T, periode)
jitter = np.random.uniform(-jitter_percent * periode, jitter_percent * periode, size=len(start_tider))
start_tider_jittered = start_tider + jitter

# Generer firkantpuls
firkantpuls = np.zeros_like(t)
for start_tid in start_tider_jittered:
    start_idx = int(start_tid * fs)
    slutt_idx = int((start_tid + puls_bredde) * fs)
    if start_idx < len(t):
        firkantpuls[start_idx:slutt_idx] = 1

# Plot firkantpulsen
plt.figure(figsize=(10, 4))
plt.plot(t, firkantpuls, label=f"Frekvens: {f} Hz, Duty cycle: {dc*100}% med jitter")
plt.title("Firkantpuls med Jitter og Konstant Pulsbredde")
plt.xlabel("Tid (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.legend()
plt.show()
