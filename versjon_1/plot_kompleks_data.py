import numpy as np
import matplotlib.pyplot as plt

# Les I/Q-data fra binærfilen
iq_data = np.fromfile("iq_data.bin", dtype=np.complex64)

# Splitte I/Q-dataene
I = iq_data.real  # Reell del (In-phase)
Q = iq_data.imag  # Imaginær del (Quadrature)

# Parametre for plotting
sampling_rate = 1000  # Sørg for at dette samsvarer med hva du brukte ved lagring
duration = len(I) / sampling_rate  # Beregn varigheten basert på antall prøver og sampling_rate
t = np.linspace(0, duration, len(I), endpoint=False)

# Plot I og Q som funksjon av tid
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(t, I, label="In-phase (I)")
plt.plot(t, Q, label="Quadrature (Q)", linestyle="--")
plt.title("I/Q Signal Components")
plt.xlabel("Tid (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()

# Plot det komplekse signalet i komplekse tallplan
plt.subplot(2, 1, 2)
plt.plot(I, Q, label="IQ Trajectory")
plt.title("I/Q Complex Plane Representation")
plt.xlabel("I (In-phase)")
plt.ylabel("Q (Quadrature)")
plt.axhline(0, color='black', linewidth=0.5, linestyle="--")
plt.axvline(0, color='black', linewidth=0.5, linestyle="--")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
