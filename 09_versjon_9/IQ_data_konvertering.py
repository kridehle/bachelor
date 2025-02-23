import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.fft import fft, fftfreq

# Funksjon som henter brukerinput, hvor brukeren kan velge om vedkommende vil benytte seg av ints eller floats
def int_eller_float():
    # Tar input,og sjekker om den er riktig. Ellers avslutts programmet
    int_float = input('\n\nVelg om du vil ha IQ data som float eller int.\nFloat32/int16\nSkirv "f" for float eller "i" for int: ')
    if int_float not in ["f","i"]:
        raise ValueError("Ugyldig input. Programmet avsluttes")
        sys.exit()
        
    return int_float


# Funksjon som lager IQ data basert på valgt bølge
def lag_IQ_data(int_float ,I_signal, Q_signal):

    # Lager IQ data som float eller int. 
    # For int så må verdiene multipliseres for at de ikke skal bli satt til null. Det fordi at
    # De aller fleste verdiene vil være plassert ut mellom 0 og 1, og alle vil da bli tolket som 0, ved en transformasjon
    # fra float til int
    if int_float == 'f':
        # Kombiner I og Q til ett datasett som float med 32 bits
        IQ_data = np.column_stack((I_signal, Q_signal)).astype(np.float32)
    else:
        # Kombinerer I og Q til ett datasett som int med 16 bits
        # Standard skaleringsverdi for en 16 bits integer
        int_skalar = 32767
        # Kombiner I og Q til ett datasett, og multipliserer verdiene med skalaren for å senere kunne transformere den til ints
        IQ_data = (np.column_stack((I_signal, Q_signal)) * int_skalar)
        
        # Finner den maksimale amplituden. Hvis ikke dataen normalfordels, ender man opp med å få verdier som er større enn 
        # En 16 bits integral sin maksgrense. Da blir verdiene bare tull
        max_amplitude = np.max(IQ_data) / int_skalar
        
        # IQ dataen tilpasses np.int16. Dette er for å forikre om at verdiene ikke overstiger +-32767
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
    #Skriver IQ data til fil som skrives til i binær modus. (write binary)
    with open (filnavn, "wb") as fil:
        fil.write(IQ_data)

    print(f"\n\nI/Q-data lagret til {filnavn}")

# Denne funksjonen har egentlig ikke noe å si for sluttproduktet til programmet, men er tiltenkt for å være en valideringsfunksjon for mennesker
# Denne funksjonen tilrettelgger for at man kan plotte det orginale signalet, hentet direkte ut fra de matematiske formlene
# Samtidig som funksjonen plotter et rekonstruert signal basert på IQ dataen som er konstruert
# I og Q plottes også hver for seg. Dette er veldig viktig for å validere at IQ dataen faktisk er korrekt
# Det blir også gjort en spektrumsanalyse av signalet som er rekonsturert, for å identifisere hvilke frekvenser som faktisk ligger i signalet
def plott_resultat(int_float, bølge_variabler):
    
    # Definerer navnet på filen med IQ data
    filnavn = "iq_data.bin"

    # Initierer listen som inneholder IQ data
    IQ_data = []
    
    # Les inn data fra binær fil og tolk det som float eller int avhenig av brukerens input
    if int_float == "f":
        # Her leses listen som om det er flyttall som er lagret i den binære filen med 32 bits lengde
        IQ_data = np.fromfile(filnavn, dtype=np.float32)    
    else: 
        # Her leses listen som om det er ints som er lagret i den binære filen. Her skaleres verdiene ned igjen til normale verdier, etter
        # å ha blitt skalert opp i første omgang, før den ble lagret
        IQ_data = np.fromfile(filnavn, dtype=np.int16) / 32767.0  

    # Split dataen i I- og Q-komponenter. I dataen er annenhver plass fra posisjon 0, og Q er annenhver plass fra posisjon 1
    I = IQ_data[::2]  
    Q = IQ_data[1::2]  

    # Lgaer en tidsvektor med hensyn på lengden av In phae komponenten (som er det samme som lengden på Quadruature komponenten)
    # og samplingsfrekvensn til signalet. 
    tidsvektor = np.arange(len(I)) / bølge_variabler[0].samplingsfrekvens   
    
    # Rekonstruer det originale signalet ved å addere sammen I og Q data
    rekonstruert_signal = I + Q 

    # Initierer valideringsbølgen
    valideringsbølge = []

    # Legger tli alle bølgene fra de forskjellgie iterasjonene til en stor bølge
    # Denne bølgen kommer til å brukes til kontrollering av det orginale
    for bølge in bølge_variabler:
        valideringsbølge = np.append(valideringsbølge, bølge.endelig_bølge)
        
        
    # Setter av en verdi som er lengden på det rekonsruerte signalet
    N = len(rekonstruert_signal)
    
    # Tar en foriertransform av det rekonsturerte signalet
    fft_rekonsturert_signal = np.fft.fft(rekonstruert_signal)
    
    # Benytter numpy sin frekvensfunksjon til å definere en x akse laget av frekvenser
    frekvenser = np.fft.fftfreq(N, d = 1/bølge_variabler[0].samplingsfrekvens)
    
    # Definerer magnitude basert på absolutt verdien av fouriertransformen
    magnitude = np.abs(fft_rekonsturert_signal) / N
        
        
    # Lag en figur med to subplotter (2 rader, 1 kolonne)
    fig, axs = plt.subplots(4, 1, figsize=(20, 12))  # To grafiske rutenett (akse)
    fig.suptitle("Visuell plot av signalene")  # Tittel for hele figuren

    # Plot rekonstruert signal på første subplot (øverste rutenett)
    axs[0].plot(tidsvektor, rekonstruert_signal, color='r', label='Rekonstruert signal')
    axs[0].set_title("Rekonstruert signal")
    axs[0].set_xlabel("Tid [s]")
    axs[0].set_ylabel("Amplitude")
    axs[0].grid(True)
    axs[0].legend()

    # Plot valideringsbølge på andre subplot (nederste rutenett)
    axs[1].plot(tidsvektor, valideringsbølge, color='b', label='Valideringsbølge')
    axs[1].set_title("Valideringsbølge")
    axs[1].set_xlabel("Tid [s]")
    axs[1].set_ylabel("Amplitude")
    axs[1].grid(True)
    axs[1].legend()


    # Plot I og Q databølger
    axs[2].plot(tidsvektor, I, color='b', label='I')
    axs[2].plot(tidsvektor, Q, color='r', label='Q')
    axs[2].set_title("I og Q data")
    axs[2].set_xlabel("Tid [s]")
    axs[2].set_ylabel("Amplitude")
    axs[2].grid(True)
    axs[2].legend()

    # Plot frekvensdomenet
    axs[3].plot(frekvenser[:N//10], magnitude[:N//10], color = 'b') 
    axs[3].set_title("Frekvensdomene")
    axs[3].set_xlabel("Frekvens [Hz]")
    axs[3].set_ylabel("Magnitude")
    axs[3].grid(True)


    # Juster plasseringen av subplottene for å unngå overlapping
    plt.tight_layout()
    
    # Justerer plass for figurtittel
    plt.subplots_adjust(top=0.9)  

    # Lagre figuren som en fil
    plt.savefig('output_bin.png')

    # Lukk plottet
    plt.close()