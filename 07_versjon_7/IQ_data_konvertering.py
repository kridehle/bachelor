import numpy as np
import matplotlib.pyplot as plt
import sys

# Funksjon som lager IQ data basert på valgt bølge
def lag_IQ_data(bølge_variabler, IQ_data_liste):

    # Lager en tidsvektor
    tidsvektor = np.arange(len(IQ_data_liste)) / bølge_variabler.samplingsfrekvens

    # Lager en bærebølge som definerer I og Q
    I_carrier = np.cos(2 * np.pi * tidsvektor)  # In-phase bærebølge
    Q_carrier = np.sin(2 * np.pi * tidsvektor)  # Quadrature bærebølge

    # Fordeler I og Q komponentene på bølgen
    I = IQ_data_liste * I_carrier  # I-komponenten
    Q = IQ_data_liste * Q_carrier  # Q-komponenten

    # Spør brukeren om vedkommende ønker int eller float.
   
    # Initierer variablen 
    int_float = ''

    # Tar input,og sjekker om den er riktig. Ellers avslutts programmet
    int_float = input('\n\nVelg om du vil ha IQ data som float eller int.\nFloat32/int16\nSkirv "f" for float eller "i" for int: ')
    if int_float not in ["f","i"]:
        raise ValueError("Ugyldig input. Programmet avsluttes")
        sys.exit()

    # Lager IQ data som float eller int. For int så må verdiene multipliseres for at de ikke skal bli satt til null
    if int_float == 'f':
        # Kombiner I og Q til ett datasett
        IQ_data = np.column_stack((I, Q)).astype(np.float32)  # 32-bit floats
    else:
        # Standard skaleringsverdi for en 16 bits integer
        int_skalar = 32767
        # Kombiner I og Q til ett datasett
        IQ_data = (np.column_stack((I, Q)) * int_skalar)# Her må det legges inn en algoritme for å finne den største amplituden
        
        # Finner den maksimale amplituden. Hvis ikke dataen normalfordels, ender man opp med å få verdier som er større enn 
        # En 16 bits integral sin maksgrense. Da blir verdiene bare tull
        max_amplitude = np.max(IQ_data) / int_skalar
        
        # IQ dataen tilpasses np.int16
        IQ_data /= max_amplitude

        # IQ dataen lagres som en np.int16
        IQ_data = IQ_data.astype(np.int16)  # Skaler fra [-1, 1] til [-32768, 32767] (må mulitpliseres med 32767 for å få riktig verdi)


        """
        NB! NB! Ved en grafisk plott av en binær fil som er laget med integraler vil tallene på y aksen
        muligens være feil. Det er ikke farlig med tanke på SDR, fordi at forholdene fortsatt er de samme
        dersom man faktisk sammenligner med valideringsbølgen.
        """
    return IQ_data

# Funksjon som skriver IQ data til en bin fil
def skriv_IQ_data(IQ_data):
    # Lagre til en .bin-fil
    filnavn = "iq_data.bin"
    #Skriver IQ data til fil
    IQ_data.tofile(filnavn)

    print(f"I/Q-data lagret til {filnavn}")


    # Funksjon som plotter resultatet slik at man kan se hvordan den binære filen skal se ut, og sammenligne det med hvordan den binære filen ser ut

# Funksjon som plotter bølgen basert på selve bølgen, og på IQ data, slik at det kan sammenlignes
def plott_resultat(bølge_variabler):
    filnavn = "iq_data.bin"  # Bytt til filen din

    # Velg int eller float
    int_float = ''

    try:
        int_float = input('\n\nVelg om du vil ha IQ data som float eller int.\nFloat32/int16\nSkirv "f" for float eller "i" for int. Dette er for å printe: ')
        if int_float not in ["f","i"]:
            raise ValueError("Ugyldig input. Programmet avsluttes")
    except ValueError as err:
        print(err)
        sys.exit()

    # Les inn data fra binær fil og tolk det som float eller int
    if int_float == "f":
        IQ_data = np.fromfile(filnavn, dtype=np.float32)    
    else: 
        IQ_data = np.fromfile(filnavn, dtype=np.int16) / 32767.0  # Normaliserer tilbake til [-1, 1]

    # Split dataen i I- og Q-komponenter
    I = IQ_data[::2]  # Hent I-komponenten (annenhver verdi)
    Q = IQ_data[1::2]  # Hent Q-komponenten (annenhver verdi)

    # Parametere for signalrekonstruksjon 
    # Samplingsfrekens (Hz), må samsvare med det opprinnelige signalet
    tidsvektor = np.arange(len(I)) / bølge_variabler[0].samplingsfrekvens   # Tidsakse

    # Genererer bærebølger for I og Q kanalen. Lager en in phase og en 90 graders faseforskøvet bærebølge
    I_carrier = np.cos(2 * np.pi * tidsvektor)  # In-phase bærebølge
    Q_carrier = np.sin(2 * np.pi * tidsvektor)  # Quadrature bærebølge

    # Demoduler for å finne I og Q
    I = I * I_carrier  # I-komponenten
    Q = Q * Q_carrier  # Q-komponenten

    # Rekonstruer det originale signalet
    rekonstruert_signal = I + Q 

    # Initierer valideringsbølgen
    valideringsbølge = np.empty(0)

    for bølge in bølge_variabler:
        valideringsbølge = np.append(valideringsbølge, bølge.endelig_bølge)

    # Lag en figur med to subplotter (2 rader, 1 kolonne)
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))  # To grafiske rutenett (akse)
    fig.suptitle("Visuell plot av signalene")  # Tittel for hele figuren

    # Plot rekonstruert signal på første subplot (øverste rutenett)
    axs[0].plot(tidsvektor, rekonstruert_signal, color='r', label='Rekonstruert signal')
    axs[0].set_title("Rekonstruert signal")
    axs[0].set_xlabel("Tid (s)")
    axs[0].set_ylabel("Amplitude")
    axs[0].grid(True)
    axs[0].legend()

    # Plot valideringsbølge på andre subplot (nederste rutenett)
    axs[1].plot(tidsvektor, valideringsbølge, color='b', label='Valideringsbølge')
    axs[1].set_title("Valideringsbølge")
    axs[1].set_xlabel("Tid (s)")
    axs[1].set_ylabel("Amplitude")
    axs[1].grid(True)
    axs[1].legend()

    # Juster plasseringen av subplottene for å unngå overlapping
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)  # Justerer plass for figurtittel

    # Lagre figuren som en fil
    plt.savefig('output_bin.png')

    # Lukk plottet
    plt.close()