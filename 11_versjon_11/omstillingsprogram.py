import variabelhenting as var
import mattefunksjoner as mat
import IQ_data_konvertering as IQ_dat
import numpy as np

# Dette er main. Hele programmet styres av denne funksjonen. Funksjoner som blir brukt i main ligger i andre programmer
# De andre programmene er: mattefunksjoner.py, variabelhenting.py, og 
def main():

    # En funksjon som henter og verifiserer variabler og lagrer de som objekter
    bølge_variabler, args = var.hent_og_verifiser_variabler()
    

    # Lager tomme lister for IQ data
    IQ_data_liste = []
    I_signal = []
    Q_signal = []

    # Itererer over alle objektene i listen og utfører funksjoner på de
    for objekt in bølge_variabler:
        
        # henter den totale tiden for gitt bølgelengde
        objekt.total_tid = mat.finn_total_tid(objekt)

        # Lager en firkantpuls som styrer pulsrepetisjonsmønsteret
        objekt.firkant_puls = mat.firkantpuls(objekt)

        # Lager en endelig bølge basert på valgt puls type og firkant puls, Lager også I og Q bølge
        objekt.endelig_bølge, I_signal_midertidig, Q_signal_midlertidig = mat.lag_endelig_bølge(objekt)

        I_signal = np.append(I_signal, I_signal_midertidig)
        Q_signal = np.append(Q_signal, Q_signal_midlertidig)

    # Lager IQ data basert på 
    IQ_data_liste = IQ_dat.lag_IQ_data(args, I_signal, Q_signal)
    
    

    # Skriver IQ data til en fil
    IQ_dat.skriv_IQ_data(IQ_data_liste,args)


    # with np.printoptions(threshold=np.inf):
    #   print(IQ_data_liste)

    # Plotter resultatet ved å sende hele objektet
    IQ_dat.plott_resultat(bølge_variabler,args)

# Passer på at main kjører først
if __name__ == "__main__":
    main()