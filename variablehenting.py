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
    Fs = variabler.get('Fs') #henter ut verdi Fs
    f = variabler.get('f') #henter uf verdi f
    s = variabler.get('s') #henter ut verdi s
    return Fs,f,s 