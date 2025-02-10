import variabelhenting
import mattefunksjoner
import numpy as np
import matplotlib.pyplot as plt
import sys

def lag_IQ_data(valgt_bølge, t):
    I_carrier = np.cos(2 * np.pi)  # In-phase bærebølge
    Q_carrier = np.sin(2 * np.pi)  # Quadrature bærebølge

    # Demoduler for å finne I og Q
    I = valgt_bølge * I_carrier  # I-komponenten
    Q = valgt_bølge * Q_carrier  # Q-komponenten

    # Kombiner I og Q til ett datasett
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
        IQ_data = np.column_stack((I, Q)).astype(np.float32)  # 32-bit floats
    else:
        IQ_data = (np.column_stack((I, Q)) * 32767).astype(np.int16)  # Skaler fra [-1, 1] til [-32768, 32767] (må mulitpliseres med 32767 for å få riktig verdi)
    return IQ_data

def skriv_IQ_data(IQ_data):
    # Lagre til en .bin-fil
    filename = "iq_data.bin"
    #Skriver IQ data til fil
    IQ_data.tofile(filename)

    print(f"I/Q-data lagret til {filename}")

# Funksjon som regner ut total tid for bølgen, slik at den kan brukes til senere funksjoner
def finn_total_tid(pulsrepetisjonsintervall, repetisjoner, duty_cycle, stagger_verdier, pri_mønster):
    # Hvis stagger benyttes så benyttes sumen av stagger verdiene + en ekstra for å få en fin graf
    if pri_mønster == 'stagger':
        gjennomsnitt_stagger_verier = (sum(stagger_verdier)) / (len(stagger_verdier))
        total_tid = sum(stagger_verdier) + gjennomsnitt_stagger_verier * 1.5
    # En så lenge får alle andre funksjoner en total tid basert på pri, repetisjoner og duty cycle
    else:
        total_tid = (pulsrepetisjonsintervall * repetisjoner) + (pulsrepetisjonsintervall * duty_cycle * 2) # Er bare for at plottet skal se fint ut. Verdien 2 kan helt fint endres, men ikke til mye mer før det kan bli problemer med antall repetisjoner
    return total_tid

# Funksjon som lager en bølge basert på valgt puls type
def lag_endelig_bølge(puls_type, firkantpuls, signalfrekvens, samplingsfrekvens, total_tid, duty_cycle, pulsrepetisjonsintervall, n_barker):
    # Her kalt for ukodet, dette er en sinusbølge.
    if puls_type == 'ukodet':
        endelig_bølge_valg = mattefunksjoner.sinusbølge(firkantpuls, pulsrepetisjonsintervall, duty_cycle, samplingsfrekvens, signalfrekvens, total_tid)
    # Her kalt for chirp, dette er en chip bøgle
    elif puls_type == 'chirp':
        print("CHIRP")
        endelig_bølge_valg = mattefunksjoner.chirpbølge(firkantpuls, signalfrekvens, samplingsfrekvens, total_tid, duty_cycle, pulsrepetisjonsintervall)
    # Her kalt for barker, dette er en barker bølge
    else:   
        print("BARKER")
        endelig_bølge_valg = mattefunksjoner.barkerbølge(firkantpuls, signalfrekvens, samplingsfrekvens, total_tid, duty_cycle, pulsrepetisjonsintervall, n_barker)
    return endelig_bølge_valg

def main():
    # Kaller opp en funksjon som leser og separerer variabler fra en fil, variabler.txt
    # Denne funksjonen returnerer en rekke forskjellige variabler som skal benyttes senere.
    samplingsfrekvens, signalfrekvens, pulsrepetisjonsintervall, duty_cycle, tid, puls_type, n_barker, pri_mønster, repetisjoner, stagger_verdier = variabelhenting.henter_variabler()
    
    # Denne variablen benyttes mye, så defineres en gang har for gjenbruk
    total_tid = finn_total_tid(pulsrepetisjonsintervall, repetisjoner, duty_cycle, stagger_verdier, pri_mønster)
    
    # Funksjon som lager en firkantpuls, basert på valgt pri mønster
    firkantpuls = mattefunksjoner.firkantpuls(pri_mønster, samplingsfrekvens, pulsrepetisjonsintervall, duty_cycle, tid, repetisjoner, total_tid, stagger_verdier)

    # Denne funksjonen genererer sluttresultatet som skal være utgangspunktet for å generere IQ data. Denne bølgen benyttre seg av en rekke andre variabler, og også resultatet av firkantpulsen
    endelig_bølge = lag_endelig_bølge(puls_type, firkantpuls, signalfrekvens, samplingsfrekvens, total_tid, duty_cycle, pulsrepetisjonsintervall, n_barker)
    
    # Denne funksjonen genererer IQ data basert på den endelige bølgen
    IQ_data = lag_IQ_data(endelig_bølge)

    # Denne funksjonen lagrer IQ data til en fil
    skriv_IQ_data(IQ_data)

    #Plotter bølgen. Dette er for å kunne kryssjekke at den binære filen er riktig
    mattefunksjoner.plott_resultat(endelig_bølge, samplingsfrekvens, signalfrekvens, total_tid)

if __name__ == "__main__":
    main()
