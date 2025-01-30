def les_fil(filnavn):
    with open(filnavn, 'r') as fil:
        innhold = fil.read().strip()
        # Fjerner kommentarer etter #
        innhold = '\n'.join([linje.split('#', 1)[0].strip() for linje in innhold.splitlines()])
        return innhold

def behandle_input(input_str):
    data = input_str.split()  # Deler inputen på mellomrom
    variabler = {}

    # Går gjennom inputen to og to elementer
    for i in range(0, len(data), 2):
        nøkkel = data[i]  # For eksempel 'a'
        verdi = data[i + 1]  # For eksempel '5'
        # Prøver å konvertere verdien til et heltall, hvis det feiler beholder vi den som en streng
        try:
            verdi = float(verdi)  # Forsøk å konvertere til heltall
        except ValueError:
            pass  # Hvis konverteringen feiler, behold verdien som en streng
        variabler[nøkkel] = verdi  # Legger til i dictionary

    return variabler
    
def henter_variabler():
    input = les_fil('variabler.txt')
    variabler=behandle_input(input)#henter ut en ordbok
    f = variabler.get('f',0) #henter uf verdi f, setter til 0 dersom ikke valgt
    if f == 0:
        f = 1e3
        print(f"Frekvens ikke angitt. Settes til {f}Hz")
    else:
        print(f"Frekvens angitt er {f}Hz")
    
    Fs = variabler.get('fs',0) #henter ut verdi Fs
    if Fs == 0:
        Skalar = 40
        Fs = Skalar * f
        print(f"Samplingsfrekvens ikke angitt. Settes til {Skalar * f}Hz")
    else:
        print(f"Samplingsfrekvens angitt er {Fs}Hz")
    
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
        
    n = int(variabler.get('n',0))
    if n == 0:
        n = 2
        print(f"Sekvens til barker ikke angitt. Verdien settes til {n}")
    else:
        print(f"Sekvens til barker angitt er {n}")
        
    mønster = variabler.get('pattern',0)
    if mønster == 0:
        mønster = 'fixed'
        print(f"PRI møsnter ikke angitt, settes til {mønster}")
    else:
        print(f"PRI mønster angitt er {mønster}")

    r = variabler.get('r',0)
    if r == 0:
        print("Antall repetisjoner ikke angitt")
    else:
        print(f"Antall repetisjoner angitt er {r}")

    return Fs,f,pri,prf,dc,t,pk,n,mønster,r
