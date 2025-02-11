import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square
from scipy.signal import chirp


# Funksjon som kan generere mange forskjellige firkantpulser avhngig av hvilken type PRI-mønster som er valgt
def firkantpuls(bølge_variabler):

    # Beregner hviletiden for sart. Spesielt viktig i sammenheng med jitter
    hvile_før_start = bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.duty_cycle * 2

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

        # Generer firkantpuls
        firkantpuls = np.zeros_like(t_lokal) # Initierer firkantpulsen
        for start_tid in start_tider_jittered: # Itererer over hver start tid i jittered signalet
            start_idx = int(start_tid * bølge_variabler.samplingsfrekvens) # Startindeks, genereres av start tid og samplingsfrekvens. Lagres som en integer
            slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens) # Sluttindeks, er det samme som start_tid + pulsbredden. Alt må mulitiplisres med samplingsfrekvens
            if start_idx < len(t_lokal): # Fortsetter løkken dersom start indeksen ikke er større en den avsluttene tiden.
                firkantpuls[start_idx:slutt_idx] = 1

        # Sett firkantpulsen til 0 frem til hviletiden
        firkantpuls[t_lokal < hvile_før_start] = 0

    # Genererer firkantpuls for en stagger bølge
    elif bølge_variabler.pri_mønster == 'stagger':
        # Definerer en lokal tidsvektor
        t_lokal = tidsvektor

        # Konverter PRI-mønsteret til en liste av float-verdier
        pri_mønster = [float(val) for val in bølge_variabler.stagger_verdier]

        firkantpuls = np.zeros_like(t_lokal)  # Initier signalet

        start_tid = 0 # Forsikrer at tiden begynner på null
        idx = 0  # Indeks for PRI-mønsteret
        while start_tid < bølge_variabler.total_tid:
            pri_nåværende = pri_mønster[idx % len(pri_mønster)]  # Hent PRI fra mønsteret (loop)
            puls_bredde = pri_nåværende * bølge_variabler.duty_cycle  # Beregn pulsbredden

            start_idx = int(start_tid * bølge_variabler.samplingsfrekvens)  # Startindeks
            slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens)  # Sluttindeks

            if start_idx < len(tidsvektor):
                firkantpuls[start_idx:slutt_idx] = 1  # Sett puls til 1

            start_tid += pri_nåværende  # Neste startpunkt
            idx += 1  # Gå til neste PRI i mønsteret
    
    # Dwell to dwell er ikke implementert enda
    elif bølge_variabler.pri_mønster == 'dwell-dwell':
        print("dwell-dwell er ikke implementert enda")

    
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

    # Finn starten av hver firkantpuls-syklus (de tidene hvor firkantbølgen går fra 0 til 1)
    syklus_starter = np.where(np.diff((bølge_variabler.firkant_puls != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer sinus som starter på nytt. (Hver gang firkatnpulsen går fra 0 til 1)
    for start in syklus_starter:
        slutt = start + int(sinus_varighet * bølge_variabler.samplingsfrekvens) # Slutt er det samme som start + varigheten på pulsen. Må gange med samplingsfrekvens for å få det riktig
        slutt = min(slutt, len(tidsvektor))  # Sørg for at vi ikke går utenfor tidsaksen

        # Beregn tidsvinduet for sinus innenfor denne syklusen
        lokal_tid = tidsvektor[start:slutt] - tidsvektor[start]  # Juster for å starte på 0
        sinus_bølge[start:slutt] = np.sin(2 * np.pi * bølge_variabler.signalfrekvens * lokal_tid)

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
        chirp_bølge[start:slutt] = chirp(tidsvektor[:slutt - start], start_frekvens, chirp_varighet, slutt_frekvens, method="linear")

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
        barker_bølge[start:slutt] = barker_bølge[start:slutt] * lokal_sinus_bølge

    return barker_bølge


# Funksjon som plotter resultatet slik at man kan se hvordan den binære filen skal se ut
def plott_resultat(bølge_variabler):
    # Plot the result

    tidsvektor = np.arange(0, bølge_variabler.total_tid, 1 / bølge_variabler.samplingsfrekvens)

    plt.figure(figsize=(10, 4))
    plt.plot(tidsvektor, bølge_variabler.endelig_bølge, label=f"(f={bølge_variabler.signalfrekvens} Hz, fs={bølge_variabler.samplingsfrekvens:.1f} Hz)",color = 'b')
    plt.title("Visuell plot")
    plt.xlabel("Tid (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.savefig('output.png')
    plt.close()
