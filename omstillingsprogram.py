import variablehenting
import mattefunksjoner

def main():
    #Kaller opp en funksjon som leser og separerer variabler fra en fil, variabler.txt
    #Denne funksjonen returnerer en rekke forskjellige variabler som skal benyttes senere.
    Fs,f,pri,prf,dc,t,pk = variablehenting.henter_variabler()
    #Funksjon som legger alle variablene inn i selve matteprogrammet, som står for den faktiske omgjøringen
    mattefunksjoner.globale_variabler(Fs,f,pri,prf,dc,t)
    #Genererer en sinusfunksjon basert på variablene som er hentet fra forrige funksjon 
    
    if pk == "ukodet":
        valgt_bølge = mattefunksjoner.sinus_bølge()
    elif pk == "chirp":
        valgt_bølge = mattefunksjoner.chirp_bølge()
    else:
        print("Pulskoden angitt eksisterer ikke, eller er ikke implementert enda. Settes til vanlig sinusbølge")
        valgt_bølge = mattefunksjoner.sinus_bølge()

    mattefunksjoner.plott_resultat(valgt_bølge)



if __name__ == "__main__":
    main()