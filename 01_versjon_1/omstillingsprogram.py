import variablehenting
import mattefunksjoner
import numpy as np

def main():
    #Kaller opp en funksjon som leser og separerer variabler fra en fil, variabler.txt
    #Denne funksjonen returnerer en rekke forskjellige variabler som skal benyttes senere.
    Fs,f,pri,prf,dc,t,pk,n,mønster = variablehenting.henter_variabler()
    #Funksjon som legger alle variablene inn i selve matteprogrammet, som står for den faktiske omgjøringen
    mattefunksjoner.globale_variabler(Fs,f,pri,prf,dc,t,n,mønster)
    #Genererer en sinusfunksjon basert på variablene som er hentet fra forrige funksjon 
    
    if pk == "ukodet":
        valgt_bølge = mattefunksjoner.sinus_bølge()
    elif pk == "chirp":
        valgt_bølge = mattefunksjoner.chirp_bølge()
    elif pk == "barker":
        valgt_bølge = mattefunksjoner.barker_bølge()
    else:
        print("Pulskoden angitt eksisterer ikke, eller er ikke implementert enda. Settes til vanlig sinusbølge")
        valgt_bølge = mattefunksjoner.sinus_bølge()

    I_carrier = np.cos(2 * np.pi *  t)  # In-phase bærebølge
    Q_carrier = np.sin(2 * np.pi *  t)  # Quadrature bærebølge

    # Demoduler for å finne I og Q
    I = valgt_bølge * I_carrier  # I-komponenten
    Q = valgt_bølge * Q_carrier  # Q-komponenten


    # Kombiner I og Q til ett datasett
    IQ_data = np.column_stack((I, Q)).astype(np.float32)  # 32-bit floats
    


    # Lagre til en .bin-fil
    filename = "iq_data_no_filter.bin"
    IQ_data.tofile(filename)

    print(f"I/Q-data lagret til {filename}")
    
    mattefunksjoner.plott_resultat(valgt_bølge)
        



if __name__ == "__main__":
    main()