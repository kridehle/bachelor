import numpy as np
from scipy.signal import square
from scipy.signal import chirp


# Funksjon som regner ut total tid for bølgen, slik at den kan brukes til senere funksjoner
def finn_total_tid(bølge_variabler):
    # Hvis stagger benyttes så benyttes sumen av stagger verdiene + en ekstra for å få en fin graf
    if bølge_variabler.pri_mønster == 'stagger':
        total_tid = sum(bølge_variabler.stagger_verdier) + bølge_variabler.pulsrepetisjonsintervall #* (1-bølge_variabler.duty_cycle) # Er bare for at plottet skal se fint ut. Verdien 2 kan helt
    
    elif bølge_variabler.pri_mønster == 'dwell':
        total_tid = 0
        
        for pri_verdi in range (len(bølge_variabler.dwell_verdier)):
            total_tid += bølge_variabler.dwell_verdier[pri_verdi] * bølge_variabler.dwell_repetisjoner[pri_verdi]


        
    

    # Pausepulsen bruker enn så lenge bare en total tid basert på pulsrepetisjonsintervall
    elif bølge_variabler.pri_mønster == 'pause' or bølge_variabler.pri_mønster == 'cw':
        total_tid = bølge_variabler.pulsrepetisjonsintervall
    
    # En så lenge får alle andre funksjoner en total tid basert på pri, repetisjoner og duty cycle
    else:
        total_tid = (bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.repetisjoner) + (bølge_variabler.pulsrepetisjonsintervall * (1 - bølge_variabler.duty_cycle)) # Er bare for at plottet skal se fint ut. Verdien 2 kan helt fint endres, men ikke til mye mer før det kan bli problemer med antall repetisjoner
    return total_tid


# Funksjon som kan generere mange forskjellige firkantpulser avhngig av hvilken type PRI-mønster som er valgt
def firkantpuls(bølge_variabler):

    # Beregner hviletiden for sart. Spesielt viktig i sammenheng med jitter
    hvile_før_start = bølge_variabler.pulsrepetisjonsintervall * 0.5

    # Beregner frekvensen for firkantpulsen
    f_firkant = 1 / bølge_variabler.pulsrepetisjonsintervall

    # Generer tidsvektor
    tidsvektor = np.arange(0, bølge_variabler.total_tid, 1 / bølge_variabler.samplingsfrekvens)
    
    # Velger en av de forskjellige PRI-mønstrene
    if bølge_variabler.pri_mønster == 'jitter':
    
        # Her er det hardkodet en jitter prosent på 10%. Denne kan gjøres variable ved behov, eller kan rett og slett endres på.
        jitter_prosent = 0.1    
        
        # Beregn pulsbredde og periode
        periode = 1 / f_firkant
        puls_bredde = bølge_variabler.duty_cycle * periode

        # Generer lokal tidsvektor
        t_lokal = np.linspace(0, bølge_variabler.total_tid, int(bølge_variabler.samplingsfrekvens * bølge_variabler.total_tid), endpoint=False)

        # Start- og sluttidspunkter for hver puls med jitter
        start_tider = np.arange(0, bølge_variabler.total_tid, periode) # Initierer signalet, og fordeler start tider jevnt utover tidsaksen basert på total tid og periode
        jitter = np.random.uniform(-jitter_prosent * periode, jitter_prosent * periode, size=len(start_tider)) # Generer en tilfeldig jitter for hver puls
        start_tider_jittered = start_tider + jitter # Setter sammen start tidene, og jitteren for å lage en komplett tilfeldig firkantpuls

        teller = 0

        # Generer firkantpuls
        firkantpuls = np.zeros_like(t_lokal) # Initierer firkantpulsen
        for start_tid in start_tider_jittered: # Itererer over hver start tid i jittered signalet
            start_idx = int(start_tid * bølge_variabler.samplingsfrekvens) # Startindeks, genereres av start tid og samplingsfrekvens. Lagres som en integer
            slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens) # Sluttindeks, er det samme som start_tid + pulsbredden. Alt må mulitiplisres med samplingsfrekvens
            firkantpuls[start_idx:slutt_idx] = 1
            if teller >= bølge_variabler.repetisjoner: # Sjekker om vi har nådd antall repetisjoner
                break
            teller += 1

        # Sett firkantpulsen til 0 frem til hviletiden
        firkantpuls[t_lokal < hvile_før_start] = 0

    # Genererer firkantpuls for en stagger bølge
    elif bølge_variabler.pri_mønster == 'stagger':
        
        # Konverter PRI-mønsteret til en liste av float-verdier
        pri_mønster = [float(val) for val in bølge_variabler.stagger_verdier]

        firkantpuls = np.zeros_like(tidsvektor)  # Initier signalet

        start_tid = 0 # Forsikrer at tiden begynner på null
        idx = 0  # Indeks for PRI-mønsteret
        while start_tid < bølge_variabler.total_tid:
            pri_nåværende = pri_mønster[idx % len(pri_mønster)]  # Hent PRI fra mønsteret (loop)
            puls_bredde = pri_nåværende * bølge_variabler.duty_cycle  # Beregn pulsbredden

            start_idx = int(start_tid * bølge_variabler.samplingsfrekvens)  # Startindeks
            slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens)  # Sluttindeks

            firkantpuls[start_idx:slutt_idx] = 1  # Sett puls til 1

            start_tid += pri_nåværende  # Neste startpunkt
            idx += 1  # Gå til neste PRI i mønsteret

            # Passer på at vi ikke lager for mange pulser
            if idx > len(bølge_variabler.stagger_verdier):
                break
    
    # Dwell to dwell er ikke implementert enda
    elif bølge_variabler.pri_mønster == 'dwell':

        # Konverterer dwell verdiene til en liste av float verdier
        pri_mønster = [float(val) for val in bølge_variabler.dwell_verdier]

        # Konverterer dwell repetisjoenr til en 
        pri_repetisjoner = [int(val) for val in bølge_variabler.dwell_repetisjoner]

        # Initierer signalet
        firkantpuls = np.zeros_like(tidsvektor)
        
        print(pri_mønster, type(pri_mønster))
        print(len(pri_mønster))
        print(pri_repetisjoner, type(pri_repetisjoner))

        start_tid = pri_mønster[0]
        teller = 1
        for sekvens in range ( len ( pri_mønster)):
            for repetisjon in range (pri_repetisjoner[sekvens]):
                
                pri_nåværende = pri_mønster[sekvens]  # Hent PRI fra mønsteret (loop)
                puls_bredde = pri_nåværende * bølge_variabler.duty_cycle  # Beregn pulsbredden

                start_idx = int(start_tid * bølge_variabler.samplingsfrekvens)  # Startindeks
                slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens)  # Sluttindeks

                firkantpuls[start_idx:slutt_idx] = 1  # Sett puls til 1

                start_tid += pri_nåværende  # Neste startpunkt








    elif bølge_variabler.pri_mønster == 'cw':
        firkantpuls = np.ones_like(tidsvektor)
    
    elif bølge_variabler.pri_mønster == 'pause':
            # Skriver null til ett array for antall punkter i tdisvektoren
        firkantpuls = np.zeros_like(tidsvektor)

    # En helt standard firkantpuls dersom ingen PRI modulering ikke er angitt
    else:
        tidsvektor = np.linspace(0, bølge_variabler.total_tid, int(bølge_variabler.samplingsfrekvens * bølge_variabler.total_tid), endpoint=False)
        firkantpuls = (square(2 * np.pi * f_firkant * tidsvektor, duty=bølge_variabler.duty_cycle) + 1) / 2
    
    return firkantpuls


# Funksjon som genererer en sinus bølge. Det er vikgit at sinusbølgen følger firkantpulsen (tror jeg)
def sinusbølge(bølge_variabler):

    
    
    # Definerer tidsvektor
    tidsvektor = np.arange(0, bølge_variabler.total_tid, 1 / bølge_variabler.samplingsfrekvens)

    # Definerer lengden på en pulsbredde
    sinus_varighet = bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.duty_cycle



    # Initier sinusbølgen
    sinus_bølge = np.zeros_like(tidsvektor)

    if bølge_variabler.pri_mønster == 'cw':
        sinus_bølge = bølge_variabler.amplitude * np.sin(2 * np.pi * bølge_variabler.signalfrekvens * tidsvektor)
        return sinus_bølge

    # Finn starten av hver firkantpuls-syklus (de tidene hvor firkantbølgen går fra 0 til 1)
    syklus_starter = np.where(np.diff((bølge_variabler.firkant_puls != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer sinus som starter på nytt. (Hver gang firkatnpulsen går fra 0 til 1)
    for start in syklus_starter:
        slutt = start + int(sinus_varighet * bølge_variabler.samplingsfrekvens) # Slutt er det samme som start + varigheten på pulsen. Må gange med samplingsfrekvens for å få det riktig
        slutt = min(slutt, len(tidsvektor))  # Sørg for at vi ikke går utenfor tidsaksen

        # Beregn tidsvinduet for sinus innenfor denne syklusen
        lokal_tid = tidsvektor[start:slutt] - tidsvektor[start]  # Juster for å starte på 0
        sinus_bølge[start:slutt] = bølge_variabler.amplitude * np.sin(2 * np.pi * bølge_variabler.signalfrekvens * lokal_tid)

    return sinus_bølge


# Funksjon som genererer en chirp bølge. Veldig lik tankegang som for sinussignalet.
def chirpbølge(bølge_variabler):
    start_frekvens = bølge_variabler.signalfrekvens # Startfrekvens
    slutt_frekvens = bølge_variabler.signalfrekvens * 10 # Avlsuttende frekvens
    
    # Pulsbreddetid defineres
    chirp_varighet = bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.duty_cycle

    # Tidsvektor defineres
    tidsvektor = np.arange(0, bølge_variabler.total_tid, 1 / bølge_variabler.samplingsfrekvens)

    # Initier chirp-signalet
    chirp_bølge = np.zeros_like(tidsvektor)

    # Finn starten av hver firkantpuls-syklus
    syklus_starter = np.where(np.diff((bølge_variabler.firkant_puls != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer chirp. Her igjen, når fikantpulsen går fra 0 til 1.
    for start in syklus_starter:
        slutt = start + int(chirp_varighet * bølge_variabler.samplingsfrekvens) # Samplingsfekvensen må mulitpliseres for å få korekkte punkter
        slutt = min(slutt, len(tidsvektor))  # Sørg for at vi ikke går utenfor tidsaksen
        # Beregn tidsvinduet for chirp innenfor denne syklusen. Bruker scipy sin chirp funksjon. Den er forhåndsdefinert
        chirp_bølge[start:slutt] = bølge_variabler.amplitude * chirp(tidsvektor[:slutt - start], start_frekvens, chirp_varighet, slutt_frekvens, method="linear")

    return chirp_bølge


# Funksjon som genererer en barker bølge
def barkerbølge(bølge_variabler):

    # Barker sekvensen
    barker_sekvens_tabell = {
        2: [1, -1],
        3: [1, 1, -1],
        4: [1, 1, -1, 1],
        5: [1, 1, 1, -1, 1],
        7: [1, 1, 1, -1, -1, 1, -1],
        11: [1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1],
        13: [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    }
    
    # Sjekker om en gyldig barker sekvens er valgt
    if bølge_variabler.n_barker not in barker_sekvens_tabell:
        raise ValueError(f"Barker kode med lengde {bølge_variabler.n_barker} finnes ikke. Verdien må være 2,3,4,5,7,11 eller 13")
        SystemExit

    # Henter ut den barker sekvensen som er definert
    barker_sekvens = barker_sekvens_tabell[bølge_variabler.n_barker]  

    # Pulsbreddetiden på signalet
    barker_varighet = bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.duty_cycle

    # Definerer tidsvektor
    tidsvektor = np.arange(0, bølge_variabler.total_tid, 1 / bølge_variabler.samplingsfrekvens)     

    # Initier Barker-signalet
    barker_bølge = np.zeros_like(tidsvektor)

    # Finn starten av hver firkantpuls-syklus. Firkantpulsen starter, eller er "på" når den ikke er 0
    syklus_starter = np.where(np.diff((bølge_variabler.firkant_puls != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer Barker-sekvensen. Når firkantpulsen går fra 0 til 1
    for start in syklus_starter:
        slutt = start + int(barker_varighet * bølge_variabler.samplingsfrekvens) # Slutt er start pluss varigheten med sampingsfekvensen
        slutt = min(slutt, len(tidsvektor))  # Sørg for at vi ikke går utenfor tidsaksen

        # Beregn antall samples per Barker-bit
        samples_per_bit = (slutt - start) // bølge_variabler.n_barker

        # Generer Barker-sekvens i dette tidsvinduet
        for i, bit in enumerate(barker_sekvens): # Henter ut plassering og verdi fra barker sekvensen i 'i' og bit
            bit_start = start + i * samples_per_bit # Definerer en start avhengig av varigheten fra tideligere bits
            bit_slutt = min(bit_start + samples_per_bit, slutt) # Beregner avsluttende tid og forsikrer om at tiden ikke passerer 'slutt' slik at vektoren blir for lang
            barker_bølge[bit_start:bit_slutt] = bit # Dette fyller en periode i barker sekvensen med en bit. Enten +1 eller -1

        # Generer lokal sinusbølge som starter på nytt for hver firkantpuls-syklus
        lokal_sinus_bølge = np.sin(2 * np.pi * bølge_variabler.signalfrekvens * (tidsvektor[start:slutt] - tidsvektor[start]))  

        # Multipliserer barker sekvensen med den lokale sinusbølgen for å modulere den
        barker_bølge[start:slutt] = barker_bølge[start:slutt] * lokal_sinus_bølge * bølge_variabler.amplitude

    return barker_bølge


# Funksjon som lager en bølge basert på valgt puls type
def lag_endelig_bølge(bølge_variabler):

    # Her kalt for ukodet, dette er en sinusbølge.
    if bølge_variabler.puls_type == 'ukodet':
        endelig_bølge_valg = sinusbølge(bølge_variabler)
    # Her kalt for chirp, dette er en chip bøgle
    elif bølge_variabler.puls_type == 'chirp':
        endelig_bølge_valg = chirpbølge(bølge_variabler)
    # Her kalt for barker, dette er en barker bølge
    elif bølge_variabler.puls_type == 'barker':   
        endelig_bølge_valg = barkerbølge(bølge_variabler)
    else:
        raise ValueError("Ugyldig puls type")
    return endelig_bølge_valg
