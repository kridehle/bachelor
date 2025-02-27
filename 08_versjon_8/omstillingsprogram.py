import variabelhenting as var
import mattefunksjoner as m
import IQ_data_konvertering as IQ_dat
import numpy as np

# Dette er main. Hele programmet styres av denne funksjonen. Funksjoner som blir brukt i main ligger i andre programmer
# De andre programmene er: mattefunksjoner.py, variabelhenting.py, og 
def main():

    # En funksjon som henter og verifiserer variabler og lagrer de som objekter
    bølge_variabler = var.hent_og_verifiser_variabler()

    # Lager en tom liste for IQ data
    IQ_data_liste = []
    I_signal = []
    Q_signal = []

    # Itererer over alle objektene i listen og utfører funksjoner på de
    for objekt in bølge_variabler:
        
        # henter den totale tiden for gitt bølgelengde
        objekt.total_tid = m.finn_total_tid(objekt)

        # Lager en firkantpuls som styrer pulsrepetisjonsmønsteret
        objekt.firkant_puls = m.firkantpuls(objekt)

        # Lager en endelig bølge basert på valgt puls type og firkant puls
        objekt.endelig_bølge, I_signal_midertidig, Q_signal_midlertidig = m.lag_endelig_bølge(objekt)

        I_signal = np.append(I_signal, I_signal_midertidig)
        Q_signal = np.append(Q_signal, Q_signal_midlertidig)

    # Lager IQ data basert på 
    IQ_data_liste = IQ_dat.lag_IQ_data(bølge_variabler[0], I_signal, Q_signal)

    # Printer IQ data listen for å validere at dataen ser forholdsmessig riktig ut
    # Det er anbefalt å ikke inkludere dette for å få en hyggelig brukeropplevelse
    # Dette er kun tenkt for å studere IQ data, for å detektere om data lages riktig eller feil
    # print(IQ_data_liste)

    # Skriver IQ data til en fil
    IQ_dat.skriv_IQ_data(IQ_data_liste)

    # Plotter resultatet ved å sende hele objektet
    IQ_dat.plott_resultat(bølge_variabler)

# Passer på at main kjører først
if __name__ == "__main__":
    main()