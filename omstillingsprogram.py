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
    #Genererer en firantpuls basert på variablene definert i variabel filen
    firkant_puls = mattefunksjoner.firkantpuls()
    #Multipliserer sammen firkantpuls og genererer en pulsbølge
    resultat = valgt_bølge * firkant_puls
    #Plotter resultatet
    mattefunksjoner.plott_resultat(resultat)



if __name__ == "__main__":
    main()