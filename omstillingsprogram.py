import variabelhenting
import mattefunksjoner
import numpy as np

def velg_bølge(pk):
    if pk == "ukodet":
        valgt_bølge = mattefunksjoner.sinus_bølge()
    elif pk == "chirp":
        valgt_bølge = mattefunksjoner.chirp_bølge()
    elif pk == "barker":
        valgt_bølge = mattefunksjoner.barker_bølge()
    else:
        print("Pulskoden angitt eksisterer ikke, eller er ikke implementert enda. Settes til vanlig sinusbølge")
        valgt_bølge = mattefunksjoner.sinus_bølge()
    return valgt_bølge

def lag_IQ_data(valgt_bølge, t):
    I_carrier = np.cos(2 * np.pi * t)  # In-phase bærebølge
    Q_carrier = np.sin(2 * np.pi * t)  # Quadrature bærebølge

    # Demoduler for å finne I og Q
    I = valgt_bølge * I_carrier  # I-komponenten
    Q = valgt_bølge * Q_carrier  # Q-komponenten

    # Kombiner I og Q til ett datasett
    IQ_data = np.column_stack((I, Q)).astype(np.float32)  # 32-bit floats
    return IQ_data

def skriv_IQ_data(IQ_data):
    # Lagre til en .bin-fil
    filename = "iq_data.bin"
    
    IQ_data.tofile(filename)

    print(f"I/Q-data lagret til {filename}")

def main():
    #Kaller opp en funksjon som leser og separerer variabler fra en fil, variabler.txt
    #Denne funksjonen returnerer en rekke forskjellige variabler som skal benyttes senere.
    Fs,f,pri,prf,dc,t,pk,n,mønster,r = variabelhenting.henter_variabler()
    #Funksjon som legger alle variablene inn i selve matteprogrammet, som står for den faktiske omgjøringen
    mattefunksjoner.globale_variabler(Fs,f,pri,prf,dc,t,n,mønster,r)
    #Velger pulskoding
    valgt_bølge = velg_bølge(pk)
    #Lager IQ data
    IQ_data = lag_IQ_data(valgt_bølge, t)
    #Lagrer IQ data
    skriv_IQ_data(IQ_data)
    #Plotter bølgen. Dette er for å kunne validere at IQ data filen er korrekt
    mattefunksjoner.plott_resultat(valgt_bølge)


if __name__ == "__main__":
    main()
