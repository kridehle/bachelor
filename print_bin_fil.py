import numpy as np
import matplotlib.pyplot as plt
import variabelhenting

#Henter variabler, men bruker egentlig bare Fs. Dette gjøres for å slippe å endre Fs manuelt for hver gang det skal printes
global Fs
Fs,f,pri,prf,dc,t,pk,n,mønster,r = variabelhenting.henter_variabler()

# Filnavnet til binærfilen
filename = "iq_data.bin"  # Bytt til filen din

# Les inn I/Q-data fra filen
IQ_data = np.fromfile(filename, dtype=np.float16)

# Split dataen i I- og Q-komponenter
I = IQ_data[::2]  # Hent I-komponenten (annenhver verdi)
Q = IQ_data[1::2]  # Hent Q-komponenten (annenhver verdi)

# Parametere for signalrekonstruksjon 
# Samplingsfrekens (Hz), må samsvare med det opprinnelige signalet
t = np.arange(len(I))/Fs   # Tidsakse

# Rekonstruer det originale signalet
reconstructed_signal = I + Q 

# Plot det rekonstruerte signalet
plt.figure(figsize=(10, 4))
plt.plot(t, reconstructed_signal, label=f"(f={f} Hz, fs={Fs:.1f} Hz)",color = 'r')
plt.title("Visuell plot")
plt.xlabel("Tid (s)")
plt.ylabel("Amplitude")
plt.grid(True)
plt.savefig('output_bin.png')
plt.close()
