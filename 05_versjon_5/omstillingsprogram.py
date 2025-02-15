import variabelhenting 
import mattefunksjoner
import numpy as np
import matplotlib.pyplot as plt
import sys

# Funksjon som henter og verifiserer variabler
def hent_og_verifiser_variabler():
    teller = 1
    bølge_variabler = variabelhenting.henter_variabler()
    for n in bølge_variabler:
        print(f"\n\nDette er bølge variablene for bølge nummer: {teller}")
        variabelhenting.BølgeVariabler.verifiser_variabler(n)

        teller += 1
    return bølge_variabler

# Funksjon som velger integer eller float
def velg_int_eller_float():
        # Spør brukeren om vedkommende ønker int eller float.
   
    # Initierer variablen 
    int_float = ''

    # Tar input,og sjekker om den er riktig. Ellers avslutts programmet
    int_float = input('\n\nVelg om du vil ha IQ data som float eller int.\nFloat32/int16\nSkirv "f" for float eller "i" for int: ')
    if int_float not in ["f","i"]:
        raise ValueError("Ugyldig input. Programmet avsluttes")
        sys.exit()
    
    return int_float

# Funksjon som lager IQ data basert på valgt bølge
def lag_IQ_data(bølge_variabler, int_float):

    # Lager en tidsvektor
    tidsvektor = np.arange(0, bølge_variabler.total_tid, 1 / bølge_variabler.samplingsfrekvens)

    # Lager en bærebølge som definerer I og Q
    I_carrier = np.cos(2 * np.pi * tidsvektor)  # In-phase bærebølge
    Q_carrier = np.sin(2 * np.pi * tidsvektor)  # Quadrature bærebølge

    # Fordeler I og Q komponentene på bølgen
    I = bølge_variabler.endelig_bølge * I_carrier  # I-komponenten
    Q = bølge_variabler.endelig_bølge * Q_carrier  # Q-komponenten

    # Lager IQ data som float eller int. For int så må verdiene multipliseres for at de ikke skal bli satt til null
    if int_float == 'f':
        # Kombiner I og Q til ett datasett
        IQ_data = np.column_stack((I, Q)).astype(np.float32)  # 32-bit floats
    else:
        # Kombiner I og Q til ett datasett
        IQ_data = (np.column_stack((I, Q)) * 32767).astype(np.int16)  # Skaler fra [-1, 1] til [-32768, 32767] (må mulitpliseres med 32767 for å få riktig verdi)

    return IQ_data

# Funksjon som skriver IQ data til en bin fil
def skriv_IQ_data(IQ_data):
    # Lagre til en .bin-fil
    filename = "iq_data.bin"
    #Skriver IQ data til fil
    IQ_data.tofile(filename)

    print(f"I/Q-data lagret til {filename}")

# Funksjon som regner ut total tid for bølgen, slik at den kan brukes til senere funksjoner
def finn_total_tid(bølge_variabler):
    # Hvis stagger benyttes så benyttes sumen av stagger verdiene + en ekstra for å få en fin graf
    if bølge_variabler.pri_mønster == 'stagger':
        total_tid = sum(bølge_variabler.stagger_verdier) + bølge_variabler.pulsrepetisjonsintervall #* (1-bølge_variabler.duty_cycle) # Er bare for at plottet skal se fint ut. Verdien 2 kan helt
    
    # Pausepulsen bruker enn så lenge bare en total tid basert på pulsrepetisjonsintervall
    elif bølge_variabler.pri_mønster == 'pause' or bølge_variabler.pri_mønster == 'cw':
        total_tid = bølge_variabler.pulsrepetisjonsintervall
    
    # En så lenge får alle andre funksjoner en total tid basert på pri, repetisjoner og duty cycle
    else:
        total_tid = (bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.repetisjoner) + (bølge_variabler.pulsrepetisjonsintervall * (1 - bølge_variabler.duty_cycle)) # Er bare for at plottet skal se fint ut. Verdien 2 kan helt fint endres, men ikke til mye mer før det kan bli problemer med antall repetisjoner
    return total_tid

# Funksjon som lager en bølge basert på valgt puls type
def lag_endelig_bølge(bølge_variabler):

    # Her kalt for ukodet, dette er en sinusbølge.
    if bølge_variabler.puls_type == 'ukodet':
        endelig_bølge_valg = mattefunksjoner.sinusbølge(bølge_variabler)
    # Her kalt for chirp, dette er en chip bøgle
    elif bølge_variabler.puls_type == 'chirp':
        endelig_bølge_valg = mattefunksjoner.chirpbølge(bølge_variabler)
    # Her kalt for barker, dette er en barker bølge
    elif bølge_variabler.puls_type == 'barker':   
        endelig_bølge_valg = mattefunksjoner.barkerbølge(bølge_variabler)
    else:
        raise ValueError("Ugyldig puls type")
    return endelig_bølge_valg

def main():

    # En funksjon som henter og verifiserer variabler og lagrer de som objekter
    bølge_variabler = hent_og_verifiser_variabler()

    # En funksjon som spør brukeren om de vil ha int eller float til IQ data
    int_eller_float = velg_int_eller_float()

    # Lager en tom liste for IQ data
    IQ_data = []

    # Administrativt
    teller = 1
    # Itererer over alle objektene i listen og utfører funksjoner på de
    for objekt in bølge_variabler:

        # Dersom det er flere enn en bølge så settes samplingsfrekvensen til den første bølgen
        if teller !=1:
            objekt.samplingsfrekvens = bølge_variabler[0].samplingsfrekvens

        # Finner total tid for bølgen
        objekt.total_tid = finn_total_tid(objekt)

        # Finner firkantpuls for bølgen
        objekt.firkant_puls = mattefunksjoner.firkantpuls(objekt)

        # Lager endelig bølge ved hjelp av firkantbølgen
        objekt.endelig_bølge = lag_endelig_bølge(objekt)

        # Lager IQ data basert på endelig bølge
        IQ_data_segment = lag_IQ_data(objekt, int_eller_float)

        # Legger til IQ data segmentet i en liste
        IQ_data.append(IQ_data_segment)

    # Konverterer listen til en numpy array
    IQ_data = np.vstack(IQ_data)

    # Skriver IQ data til en binær fil
    skriv_IQ_data(IQ_data)

    # Plotter resultatet ved å sende hele objektet
    mattefunksjoner.plott_resultat(bølge_variabler)

# Passer på at main kjører først
if __name__ == "__main__":
    main()
