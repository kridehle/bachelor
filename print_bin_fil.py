import numpy as np
import matplotlib.pyplot as plt
import variabelhenting
import sys


#Henter variabler, men bruker egentlig bare Fs. Dette gjøres for å slippe å endre Fs manuelt for hver gang det skal printes
global Fs
Fs,f,pri,dc,t,pk,n,mønster,r,stagger_verdier = variabelhenting.henter_variabler()

# Filnavnet til binærfilen
filename = "iq_data.bin"  # Bytt til filen din

# Velg int eller float

int_float = ''

try:
    int_float = input('\n\nVelg om du vil ha IQ data som float eller int.\nFloat32/int16\nSkirv "f" for float eller "i" for int: ')
    if int_float not in ["f","i"]:
        raise ValueError("Ugyldig input. Programmet avsluttes")
except ValueError as err:
    print(err)
    sys.exit()


# Les inn data fra binær fil og tolk det som float eller int
if int_float == "f":
    IQ_data = np.fromfile(filename, dtype=np.float32)    
else: 
    IQ_data = np.fromfile(filename, dtype=np.int16) / 32767.0  # Normaliserer tilbake til [-1, 1]
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
