import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square
from scipy.signal import chirp

def globale_variabler(Fs,F,Pri,Prf,Dc,T):
    #setter global samplingsfrekvens
    global fs
    fs = Fs
    #setter global signalfrekvens
    global f
    f = F
    #setter global pri
    global pri
    pri = Pri
    #setter global prf
    global prf 
    prf = Prf
    #Setter global firkantpulsfrekvens. Den defineres av PRI/PRF
    global f_firkant
    try:
        # Validere at prf og pri er floats
        prf = float(prf) if prf is not None else 0
        pri = float(pri) if pri is not None else 0
        # Hvis ingen av variablene er satt, settes frekvensen på fikrantpulsen via
        # Frekvensen dividert på 100
        # Dette er for at en bruker skal kunne bruke PRI eller PRF avhengig av hva de 
        # liker best
        if prf == 0 and pri == 0:
            print(f"PRI/PRF ikke angtt. Setter PRF = {f} / 100")
            prf = f / 100
            f_firkant = prf
        elif prf != 0 and pri == 0:
            # Hvis PRF er angitt, og ikke PRI
            f_firkant = prf
        elif pri != 0:
            # Hvis PRI er angitt, og ikke PRF
            f_firkant = 1 / pri
        else:
            raise ValueError("Unexpected values for PRF and PRI.")
    except ZeroDivisionError:
        print("Error: PRI cannot be zero when calculating frequency.")
    except Exception as e:
        print(f"An error occurred: {e}")
        
    #setter global duty cycle
    global dc 
    dc = Dc
    
    #Setter pulsbreddetid. Denne skal brukes til blant annet chirp
    #Perioden til et firkantsignal er angitt av 1/f. Ganger man det med dutycycle
    #Vil man få tiden til 
    global pwt
    pwt = (1/f_firkant)*dc 
    print(f"Pw er {pwt}")
    
    #Definerer felles tidsvektor
    global t
    t = np.arange(0, T, 1 / fs)
    

#Funksjon som lager en helt standard sinusbølge
def sinus_bølge():
    # Genererer sinusbølge
    sinus_bølge = np.sin(2 * np.pi * f * t)
    #Returnerer den genererte sinusbølgen
    return sinus_bølge

#Funksjon som genererer en firkantpuls. Frekvens og duty cycle defineres av variablene i inputen. Hvis ingen 
#ønskede verdier er gitt, settes det forhåndsdefinerte verdier.
def firkantpuls():  
    #Generering av firkantpuls. Frekvensen defineres av prf/pri, og duty cycle styres av ønsket verdi.
    #Adderer med 1, og dividerer med 2 for å sette pulsen på 1 (på), og deretter 0 (av). 
    #Dette for å kunne skru signalet av og på, og sende pulser.
    firkantpuls = (square(2 * np.pi * f_firkant * t, duty=dc)+1)/2
    return firkantpuls


def chirp_bølge():
    f0 = f
    f1 = 5*f
    chirp_bølge = chirp(t, f0=f0, t1=pwt, f1=f1, method='linear', phi=0)
    return chirp_bølge


#Funksjon som plotter resultatet
def plott_resultat(final_wave):
    # Plot the result
    plt.figure(figsize=(10, 4))
    plt.plot(t, final_wave, label=f"(f={f} Hz, fs={fs:.1f} Hz)")
    plt.title("Visuell plot")
    plt.xlabel("Tid (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

