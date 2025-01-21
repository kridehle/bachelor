import ast

def les_fra_fil():#Funksjon som leser all data fra en fil, og separerer linjer.
    file = open("variabler.txt", "r")#åpner variablefil i lesemodus
    innhold = file.read()#lagrer innholdet i filen i content
    file.close()#lukker filen
    innhold = innhold.splitlines()#separerer linjer i content
    return innhold

def hent_ut_variabler():#henter ut filer fra conten, og lager en ordliste
    verdier = {}#ordlisten lages
    innhold = les_fra_fil()#kaller opp les fra fil, og legger innholdet i content

    for linje in innhold:#går gjennom alle linjer i content

        linje = linje.split("#", 1)[0].strip()#kommentarer markeres av en #. Alt etter # ignoreres

        if not linje: #sparer prosessorkraft med å ikke prsessere tomme linjer
            continue

        linje = linje.strip() #fjerner mellomrom
        if "=" in linje: #identifiserer variabler hvis det er = i linjen
            navn, verdi = linje.split("=",1)#splitter navn og verdier. = er markøren
            navn = navn.strip()#tar bort mellomrom fra navn
            navn = navn.lower()#gjør alt til små bokstaver, for å fjerne case sensitivitet
            verdi = verdi.strip()#tar bort mellomrom fra verdi
            try:
                verdi = eval(verdi)
            except:
                pass
            verdier[navn] = verdi

    return verdier #returnerer en ordbok
    
def separer_variabler():
    variabler=hent_ut_variabler()#henter ut en ordbok
    f = variabler.get('f',0) #henter uf verdi f, setter til 0 dersom ikke valgt
    if f == 0:
        print("Frekvens ikke angitt. Settes til 1kHz")
        f = 1e3
    
    Fs = variabler.get('fs',0) #henter ut verdi Fs
    if Fs == 0:
        Fs = 20 * f
        print("Samplingsfrekvens ikke angitt. Settes til 20 * f")
    s = variabler.get('s') #henter ut verdi s
    
    pri = variabler.get('pri',0)
    if pri == 0:
        print("PRI ikke angitt.")
    
    prf = variabler.get('prf',0)
    if prf == 0:
        print("PRF ikke angitt.")
    
    dc = variabler.get('dc',0)
    if dc == 0:
        print("Dutycycle ikke angitt. Setts til 0.1")
    
    t = variabler.get('t',0)
    if t == 0:
        print("Ønsket tid ikke angitt. Settes til 0.1s")    
    
    return Fs,f,pri,prf,dc,t
