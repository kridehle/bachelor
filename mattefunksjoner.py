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
    #Vil man få varigheten til en enkelt puls
    global pwt
    pwt = (1/f_firkant)*dc 
    print(f"Pw er {pwt}")
    
    #Definerer felles tidsvektor
    global t
    t = np.arange(0, T, 1 / fs)
    
    global barker_lengde
    barker_lengde = 7
    
#Funksjon som lager en helt standard sinusbølge
def sinus_bølge():
    # Genererer sinusbølge
    sinus_bølge = np.sin(2 * np.pi * f * t)
    #Returnerer den genererte sinusbølgen
    modulert_bølge = sinus_bølge * firkantpuls()
    return modulert_bølge

#Funksjon som genererer en firkantpuls. Frekvens og duty cycle defineres av variablene i inputen. Hvis ingen 
#ønskede verdier er gitt, settes det forhåndsdefinerte verdier.
def firkantpuls():  
    #Generering av firkantpuls. Frekvensen defineres av prf/pri, og duty cycle styres av ønsket verdi.
    #Adderer med 1, og dividerer med 2 for å sette pulsen på 1 (på), og deretter 0 (av). 
    #Dette for å kunne skru signalet av og på, og sende pulser.
    firkantpuls = (square(2 * np.pi * f_firkant * t, duty=dc)+1)/2
    return firkantpuls

# Funksjon for en pulskodet bølge. Chirp bølge
def chirp_bølge():
    f0 = f #Frekvensen f0 er startfrekvesn
    f1 = 10*f #Frekvensen f1 er sluttfrekvens
    firkant_bølge = firkantpuls() #Henter inn firkantbølge for å kunne sende chirp i pulser
    chirp_varighet = pwt #Varigheten er det samme som tiden til en pulsbredde
    
    # Initier chirp-signalet
    ch_bølge = np.zeros_like(t)

    # Finn starten av hver firkantpuls-syklus
    syklus_starter = np.where(np.diff((firkant_bølge != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer chirp
    for start in syklus_starter:
        slutt = start + int(chirp_varighet * fs)
        slutt = min(slutt, len(t))  # Sørg for at vi ikke går utenfor tidsaksen
        # Beregn tidsvinduet for chirp innenfor denne syklusen
        ch_bølge[start:slutt] = chirp(
            t[:slutt - start], f0, chirp_varighet, f1, method="linear"
        )

    return ch_bølge

# Funksjon som inneholder forskjellige barker sekvenser
def barker_kode(n):
    barker_sekvens = {
        2: [1, -1],
        3: [1, 1, -1],
        4: [1, 1, -1, 1],
        5: [1, 1, 1, -1, 1],
        7: [1, 1, 1, -1, -1, 1, -1],
        11: [1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1],
        13: [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    }
    
    if n not in barker_sekvens:
        raise ValueError(f"Barker kode med lengde {n} finnes ikke. Verdien må være 2,3,4,5,7,11 eller 13")
    return barker_sekvens[n]



    return combined_wave

# Funksjon som genererer et barker kodet signal
def barker_bølge():
    n = 2 # Lengden på Barker-koden (kan endres ved behov)
    barker_sekvens = barker_kode(n)  # Hent Barker-koden og lagrer en variant av den
    firkant_bølge = firkantpuls()  # Hent firkantpulsen for å styre aktivering
    barker_varighet = pwt  # Varigheten til en Barker-sekvens er lik en pulsbredde
                           # Samme tankegang som med Chirp

    # Initier Barker-signalet
    barker_bølge = np.zeros_like(t)

    # Finn starten av hver firkantpuls-syklus. Firkantpulsen starter, eller er "på" når den ikke er 0
    syklus_starter = np.where(np.diff((firkant_bølge != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer Barker-sekvensen
    for start in syklus_starter:
        slutt = start + int(barker_varighet * fs)
        slutt = min(slutt, len(t))  # Sørg for at vi ikke går utenfor tidsaksen

        # Beregn antall samples per Barker-bit
        samples_per_bit = (slutt - start) // n

        # Generer Barker-sekvens i dette tidsvinduet
        for i, bit in enumerate(barker_sekvens):
            bit_start = start + i * samples_per_bit
            bit_slutt = min(bit_start + samples_per_bit, slutt)
            barker_bølge[bit_start:bit_slutt] = bit

    barker_bølge = barker_bølge * sinus_bølge()
    return barker_bølge

#Funksjon som plotter resultatet
def plott_resultat(final_wave):
    # Plot the result
    # plt.style.use('dark_background')
    plt.figure(figsize=(10, 4))
    plt.plot(t, final_wave, label=f"(f={f} Hz, fs={fs:.1f} Hz)")
    
    plt.title("Visuell plot")
    plt.xlabel("Tid (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

