import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square


#Funksjon som lager en helt standard sinusbølge
def sinus_bølge(fs, f, varighet):
    #Sjekker om det er en ønsket tid angitt. Dersom det ikke er angitt noen tid
    #settes tiden til 0.1s. Hvis ikke står den urørt. Tiden settes som en global variabel for
    #å være lik for alle funksjoner.
    global tid
    if varighet == 0:
        tid = 0.1
    else:    
        tid = varighet
    
    #Definerer tidsvektoren
    global t
    t = np.arange(0, tid, 1 / fs)

    # Genererer sinusbølge
    sinus_bølge = np.sin(2 * np.pi * f * t)

    #Returnerer den genererte sinusbølgen
    return sinus_bølge

#Funksjon som genererer en firkantpuls. Frekvens og duty cycle defineres av variablene i inputen. Hvis ingen 
#ønskede verdier er gitt, settes det forhåndsdefinerte verdier.
def firkantpuls(fs,f,pri,prf,duty_cycle):  
    #sjekker om det er verdier spesifisert. Dersom ikke settes PRF til f/100

    try:
        if prf == 0 & pri == 0:
            print("PRI/PRF ikke angitt. Setter PRF = f/100")
            prf = f/100
            frequency_square = prf
    except:
        #Dersom vi har prf og ikke pri, brukes prf      
        if pri == 0:
            frequency_square = prf  # frequency (Hz)
        #Dersom vi har pri og ikke prf brukes pri
        else:
            frequency_square = 1/pri

    #Dersom dutycycle ikke er definert, settes den til en standardverdi her
    if duty_cycle == 0:
        duty_cycle = 0.1  # Prosent av tiden hvor signalet er på
        
    #Generering av firkantpuls. Frekvensen defineres av prf/pri, og duty cycle styres av ønsket verdi.
    #Adderer med 1, og dividerer med 2 for å sette pulsen på 1 (på), og deretter 0 (av). 
    #Dette for å kunne skru signalet av og på, og sende pulser.
    firkantpuls = (square(2 * np.pi * frequency_square * t, duty=duty_cycle)+1)/2
    return firkantpuls

#Funksjon som plotter resultatet
def plott_resultat(final_wave,f,fs):
    # Plot the result
    plt.figure(figsize=(10, 4))
    plt.plot(t, final_wave, label=f"Sinusbølge modulert av firkantpuls (f={f} Hz, fs={fs:.1f} Hz)")
    plt.title("Sinusbølge modulert av firkantpuls")
    plt.xlabel("Tid (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.show()

