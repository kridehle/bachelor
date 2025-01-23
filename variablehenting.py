import ast

def les_fra_fil():#Funksjon som leser all data fra en fil, og separerer linjer.
    file = open("variabler.txt", "r")#åpner variablefil i lesemodus
    innhold = file.read()#lagrer innholdet i filen i content
    file.close()#lukker filen
    innhold = innhold.splitlines()#separerer linjer i content
    return innhold

def separerer_variabler():#henter ut filer fra conten, og lager en ordliste
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
    
def henter_variabler():
    variabler=separerer_variabler()#henter ut en ordbok
    f = variabler.get('f',0) #henter uf verdi f, setter til 0 dersom ikke valgt
    if f == 0:
        f = 1e3
        print(f"Frekvens ikke angitt. Settes til {f}Hz")
    else:
        print(f"Frekvens angitt er {f}Hz")
    
    Fs = variabler.get('fs',0) #henter ut verdi Fs
    if Fs == 0:
        a = 40
        Fs = a * f
        print(f"Samplingsfrekvens ikke angitt. Settes til {a} * {f}Hz")
    else:
        print(f"Samplingsfrekvens angitt er {Fs}Hz")
    
    s = variabler.get('s') #henter ut verdi s
    
    pri = variabler.get('pri',0)
    if pri == 0:
        print("PRI ikke angitt.")
    else:
        print(f"PRI angitt er {pri}s")
    
    prf = variabler.get('prf',0)
    if prf == 0:
        print("PRF ikke angitt.")
    else:
        print(f"PRF angitt er {prf}Hz")

    dc = variabler.get('dc',0)
    if dc == 0:
        dc = 0.1
        print(f"Dutycycle ikke angitt. Setts til {dc}")
    else:
        print(f"Dutycycle angitt er {dc}")
    
    t = variabler.get('t',0)
    if t == 0:
        t = 0.1
        print(f"Tid ikke angitt. Settes til {t}s")  
    else:
        print(f"Tid angitt er {t}s")
    
    pk = variabler.get('pk', 'ukodet')    
    if pk == 'ukodet':
        print(f"Pulskoding ikke definert, settes til {pk}")
    else:
        print(f"Pulskoding angitt er {pk}")
            
    
    return Fs,f,pri,prf,dc,t,pk
