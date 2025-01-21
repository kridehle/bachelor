import ast

def les_fra_fil():#Funksjon som leser all data fra en fil, og separerer linjer.
    file = open("variabler.txt", "r")#åpner variablefil i lesemodus
    content = file.read()#lagrer innholdet i filen i content
    file.close()#lukker filen
    content = content.splitlines()#separerer linjer i content
    return content

def hent_ut_variabler():#henter ut filer fra conten, og lager en ordliste
    values = {}#ordlisten lages
    content = les_fra_fil()#kaller opp les fra fil, og legger innholdet i content

    for line in content:#går gjennom alle linjer i content

        line = line.split("#", 1)[0].strip()#kommentarer markeres av en #. Alt etter # ignoreres

        if not line: #sparer prosessorkraft med å ikke prsessere tomme linjer
            continue

        line = line.strip() #fjerner mellomrom
        if "=" in line: #identifiserer variabler hvis det er = i linjen
            name, value = line.split("=",1)#splitter navn og verdier. = er markøren
            name = name.strip()#tar bort mellomrom fra navn
            value = value.strip()#tar bort mellomrom fra verdi
            try:
                value = eval(value)
            except:
                pass
            values[name] = value

    return values #returnerer en ordbok
    
def separer_variabler():
    variabler=hent_ut_variabler()#henter ut en ordbok
    Fs = variabler.get('Fs',0) #henter ut verdi Fs
    if Fs == 0:
        print("Samplingsfrekvens ikke angitt. Settes til 20 * f")
    f = variabler.get('f',0) #henter uf verdi f
    if f == 0:
        print("Frekvens ikke angitt. Settes til 1kHz")
        f = 1e3
    s = variabler.get('s') #henter ut verdi s
    pri = variabler.get('PRI',0)
    if pri == 0:
        print("PRI ikke angitt. Settes ikke")
    prf = variabler.get('PRF',0)
    if prf == 0:
        print("PRF ikke angitt. Settes ikke")
    dc = variabler.get('DC',0)
    return Fs,f,pri,prf,dc
