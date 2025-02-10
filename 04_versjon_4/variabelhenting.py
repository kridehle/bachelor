import sys

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
            verdi = int(verdi)  # Forsøk å konvertere til heltall
        except ValueError:
            try:
                verdi = float(verdi)
            except:
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
        Skalar = 8000
        Fs = Skalar * f
        print(f"Samplingsfrekvens ikke angitt. Settes til {Skalar * f}Hz")
    else:
        print(f"Samplingsfrekvens angitt er {Fs}Hz")
    
    pri = variabler.get('pri',0)
    prf = variabler.get('prf',0)

    if pri == 0 and prf == 0:
        pri = (1/f) * 10
        print(f"PRI og PRF er ikke angitt. PRI settes til {pri}s")
    elif pri != 0 and prf == 0:
        print(f"PRI angitt er {pri}s")
    elif pri == 0 and prf != 0:    
        print(f"PRF angitt er {prf}Hz")
        pri = 1 / prf     

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
    

    mønster = variabler.get('mønster', 'nil')    

    deler = mønster.split(',')
    mønster = deler [0]
    stagger_verdier = deler[1:]
    stagger_verdier = list(map(float, stagger_verdier))


    if mønster == 'stagger':
        print(f"Stagger verdier angitt er {stagger_verdier}s")

    if mønster == 'nil':
        mønster = 'ukodet'
        print(f"Pulskoding ikke angitt. Pulskoding settes til er {mønster}")
    elif mønster != 'ukodet' and mønster != 'stagger' and mønster != 'jitter' and mønster != 'dwell-dwell':
        raise ValueError("Feil pulskode angitt. Benytt deg av en gyldig pulskode eller hold feltet åpent")
        SystemExit
    else:
        print(f"Pulskoding angitt er {mønster}")


    n = int(variabler.get('n',0))
    if n == 0:
        n = 2
        print(f"Sekvens til barker ikke angitt. Verdien settes til {n}")
    else:
        print(f"Sekvens til barker angitt er {n}")
        
    pulskode = variabler.get('pk',0)
    if pulskode == 0:
        pulskode = 'ukodet'
        print(f"PRI pulskode ikke angitt, settes til {pulskode}")
    elif pulskode != 'ukodet' and pulskode != 'chirp' and pulskode != 'barker':
        raise ValueError("Feil pulskode/modulering angitt. Benytt deg av en gyldig pulskode eller hold feltet åpent")
        SystemExit
    else:
        print(f"PRI pulskode angitt er {pulskode}")

    r = variabler.get('r',0)
    if r == 0:
        print("Antall repetisjoner ikke angitt")
    else:
        print(f"Antall repetisjoner angitt er {r}")

    return Fs,f,pri,dc,t,pulskode,n,mønster,r, stagger_verdier
