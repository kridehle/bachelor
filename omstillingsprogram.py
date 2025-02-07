import variabelhenting
import mattefunksjoner
import numpy as np
import matplotlib.pyplot as plt
import sys

def lag_IQ_data(valgt_bølge, t):
    I_carrier = np.cos(2 * np.pi * t)  # In-phase bærebølge
    Q_carrier = np.sin(2 * np.pi * t)  # Quadrature bærebølge

    # Demoduler for å finne I og Q
    I = valgt_bølge * I_carrier  # I-komponenten
    Q = valgt_bølge * Q_carrier  # Q-komponenten

    # Kombiner I og Q til ett datasett
    # Spør brukeren om vedkommende ønker int eller float.
   
    # Initierer variablen 
    int_float = ''

    try:
        int_float = input('\n\nVelg om du vil ha IQ data som float eller int.\nFloat32/int16\nSkirv "f" for float eller "i" for int: ')
        if int_float not in ["f","i"]:
            raise ValueError("Ugyldig input. Programmet avsluttes")
    except ValueError as err:
        print(err)
        sys.exit()
     
    # Lager IQ data som float eller int. For int så må verdiene multipliseres for at de ikke skal bli satt til null
    if int_float == 'f':
        IQ_data = np.column_stack((I, Q)).astype(np.float32)  # 32-bit floats
    else:
        IQ_data = (np.column_stack((I, Q)) * 32767).astype(np.int16)  # Skaler fra [-1, 1] til [-32768, 32767]

    return IQ_data

def skriv_IQ_data(IQ_data):
    # Lagre til en .bin-fil
    filename = "iq_data.bin"
    
    IQ_data.tofile(filename)

    print(f"I/Q-data lagret til {filename}")

def finn_total_tid(pulsrepetisjonsintervall, repetisjoner, duty_cycle, stagger_verdier, pri_mønster):
    if pri_mønster == 'stagger':
        gjennomsnitt_stagger_verier = (sum(stagger_verdier)) / (len(stagger_verdier))
        total_tid = sum(stagger_verdier) + gjennomsnitt_stagger_verier * 1.5
    else:
        total_tid = (pulsrepetisjonsintervall * repetisjoner) + (pulsrepetisjonsintervall * duty_cycle * 2) # Er bare for at plottet skal se fint ut. Verdien 3 kan helt fint endre, men ikke til mye mer før det kan bli problemer med antall repetisjoner
    return total_tid

def lag_endelig_bølge(puls_type, firkantpuls, signalfrekvens, samplingsfrekvens, total_tid, duty_cycle, pulsrepetisjonsintervall, n_barker):
    if puls_type == 'ukodet':
        endelig_bølge_valg = mattefunksjoner.sinusbølge(firkantpuls, pulsrepetisjonsintervall, duty_cycle, samplingsfrekvens, signalfrekvens, total_tid)
    elif puls_type == 'chirp':
        print("CHIRP")
        endelig_bølge_valg = mattefunksjoner.chirpbølge(firkantpuls, signalfrekvens, samplingsfrekvens, total_tid, duty_cycle, pulsrepetisjonsintervall)
    else:   
        print("BARKER")
        endelig_bølge_valg = mattefunksjoner.barkerbølge(firkantpuls, signalfrekvens, samplingsfrekvens, total_tid, duty_cycle, pulsrepetisjonsintervall, n_barker)
    return endelig_bølge_valg

def main():
    #Kaller opp en funksjon som leser og separerer variabler fra en fil, variabler.txt
    #Denne funksjonen returnerer en rekke forskjellige variabler som skal benyttes senere.
    samplingsfrekvens, signalfrekvens, pulsrepetisjonsintervall, duty_cycle, tid, puls_type, n_barker, pri_mønster, repetisjoner, stagger_verdier = variabelhenting.henter_variabler()
    
    #Denne variablen benyttes mye, så defineres en gang har for gjenbruk
    total_tid = finn_total_tid(pulsrepetisjonsintervall, repetisjoner, duty_cycle, stagger_verdier, pri_mønster)
    
    firkantpuls = mattefunksjoner.firkantpuls(pri_mønster, samplingsfrekvens, pulsrepetisjonsintervall, duty_cycle, tid, repetisjoner, total_tid, stagger_verdier)

    endelig_bølge = lag_endelig_bølge(puls_type, firkantpuls, signalfrekvens, samplingsfrekvens, total_tid, duty_cycle, pulsrepetisjonsintervall, n_barker)
    

    IQ_data = lag_IQ_data(endelig_bølge, total_tid)
    #Lagrer IQ data
    skriv_IQ_data(IQ_data)
    #Plotter bølgen. Dette er for å kunne validere at IQ data filen er korrekt
    mattefunksjoner.plott_resultat(endelig_bølge, samplingsfrekvens, signalfrekvens, total_tid)

if __name__ == "__main__":
    main()
