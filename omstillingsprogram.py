import variablehenting
import mattefunksjoner

def main():
    #Kaller opp en funksjon som leser og separerer variabler fra en fil, variabler.txt
    #Denne funksjonen returnerer en rekke forskjellige variabler som skal benyttes senere.
    Fs,f,pri,prf,dc,t = variablehenting.separer_variabler()
    
    #Genererer en sinusfunksjon basert på variablene som er hentet fra forrige funksjon 
    sinus_bølge = mattefunksjoner.sinus_bølge(Fs,f,t)
    #Genererer en firantpuls basert på variablene definert i variabel filen
    firkant_puls = mattefunksjoner.firkantpuls(Fs,f,pri,prf,dc)
    #Multipliserer sammen firkantpuls og genererer en pulsbølge
    resultat = sinus_bølge * firkant_puls
    #Plotter resultatet
    mattefunksjoner.plott_resultat(resultat,f,Fs)



if __name__ == "__main__":
    main()