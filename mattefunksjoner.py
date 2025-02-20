import numpy as np
from scipy.signal import square
from scipy.signal import chirp


# Funksjon som regner ut total tid for bølgen, slik at den kan brukes til senere funksjoner
def finn_total_tid(bølge_variabler):
    # Hvis stagger benyttes så benyttes sumen av stagger verdiene + en ekstra for å få en fin graf
    if bølge_variabler.pri_mønster == 'stagger':
        total_tid = sum(bølge_variabler.stagger_verdier) #+ bølge_variabler.stagger_verdier[len(bølge_variabler.stagger_verdier) - 1] #* (1-bølge_variabler.duty_cycle) # Er bare for at plottet skal se fint ut. Verdien 2 kan helt
    
    # Hvis dwell - dwell brukes regnes tidsvektoren ut på følgende måte
    elif bølge_variabler.pri_mønster == 'dwell':

        # Initierer total tid
        total_tid = 0
        
        # Itererer n ganger (lengden) på inputen. Og ganger pri tider med repetissjoner
        for pri_verdi in range (len(bølge_variabler.dwell_verdier)):
            total_tid += bølge_variabler.dwell_verdier[pri_verdi] * bølge_variabler.dwell_repetisjoner[pri_verdi]
        

    # Pausepulsen bruker enn så lenge bare en total tid basert på pulsrepetisjonsintervall
    elif bølge_variabler.pri_mønster == 'pause' or bølge_variabler.pri_mønster == 'cw':
        total_tid = bølge_variabler.pulsrepetisjonsintervall
    
    # Jitter og fixed får følgende total tid
    else:
        total_tid = (bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.repetisjoner) #+ (bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.duty_cycle) # Er bare for at plottet skal se fint ut. Verdien 2 kan helt fint endres, men ikke til mye mer før det kan bli problemer med antall repetisjoner
    
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
        # Initierer signalet, og fordeler start tider jevnt utover tidsaksen basert på total tid og periode
        start_tider = np.arange(0, bølge_variabler.total_tid, periode) 
        
        # Generer en tilfeldig jitter for hver puls. Jitter prosenten avgjør hvor store forskjeller det er. Er ikke angitt jitter prosent ønsket byttes den bare ut
        jitter = np.random.uniform(-jitter_prosent * periode, jitter_prosent * periode, size=len(start_tider))

        # Setter sammen start tidene, og jitteren for å lage en komplett tilfeldig firkantpuls
        start_tider_jittered = start_tider + jitter 

        # Initierer en teller
        teller = 0

        # Initierer firkantpulsen
        firkantpuls = np.zeros_like(t_lokal)

        # Itererer over hver start tid i jittered signalet
        for start_tid in start_tider_jittered: 

            # Startindeks, genereres av start tid og samplingsfrekvens. Lagres som en int
            start_idx = int(start_tid * bølge_variabler.samplingsfrekvens)

            # Sluttindeks, er det samme som start_tid + pulsbredden. Alt må mulitiplisres med samplingsfrekvens
            slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens)

            # Det er faktisk her firkantpulsen får verdier. Den settes til 1 mellom start og slutt av en puls 
            firkantpuls[start_idx:slutt_idx] = 1

            # Sjekker om vi har nådd antall repetisjoner
            if teller >= bølge_variabler.repetisjoner: 
                break
            teller += 1

        # Sett firkantpulsen til 0 frem til hviletiden
        firkantpuls[t_lokal < hvile_før_start] = 0

    # Genererer firkantpuls for en stagger bølge
    elif bølge_variabler.pri_mønster == 'stagger':
        
        # Konverter PRI-mønsteret til en liste av float-verdier
        pri_mønster = [float(val) for val in bølge_variabler.stagger_verdier]

        # Initier signalet
        firkantpuls = np.zeros_like(tidsvektor)  

        # Forsikrer at tiden ikke begynner på null, fordi da er det ikke sikkert senere bølge fanger opp at den går fra 0 til 1
        start_tid = tidsvektor[1]

        # Gjennomgår for hvert eneste pri_mønster angitt
        for repetisjon in range (len(pri_mønster)):
            
            # Hent PRI fra mønsteret for gjeldende iterasjon
            pri_nåværende = pri_mønster[repetisjon]  

            # Beregn pulsbredden
            puls_bredde = pri_nåværende * bølge_variabler.duty_cycle  

            # Startindeks
            start_idx = int(start_tid * bølge_variabler.samplingsfrekvens)  

            # Sluttindeks
            slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens)  
            
            # Det er faktisk her firkantpulsen får verdier. Den settes til 1 mellom start og slutt av en puls
            firkantpuls[start_idx:slutt_idx] = 1  

            # Neste startpunkt
            start_tid += pri_nåværende


    # Firkantpuls som lager bølger basert på dwell to dwell 
    elif bølge_variabler.pri_mønster == 'dwell':

        # Konverterer dwell verdiene til en liste av float verdier
        # Dette er egentlig allerede gjort, men det må gjøres her av en eller annen grunn også. Dette skal undersøkes videre
        pri_mønster = [float(val) for val in bølge_variabler.dwell_verdier]

        # Konverterer dwell repetisjoenr til en 
        # Same her
        pri_repetisjoner = [int(val) for val in bølge_variabler.dwell_repetisjoner]

        # Initierer signalet
        firkantpuls = np.zeros_like(tidsvektor)
        
        # Setter at første puls ikke begynner momentant, men begynner etter en viss periode som da er gitt av en pri lengde
        start_tid = tidsvektor[1]

        # En administrativ teller
        teller = 1

        # Løkke som itererer over antall pri sekvenser som er angitt
        for sekvens in range ( len ( pri_mønster)):

            # Løkke som itererer over antall repetisjoner som er angitt av nåværende repetisjonsfaktor
            for repetisjon in range (pri_repetisjoner[sekvens]):
                
                # Nåværende PRI hentes fra pri_mønster som er floatversjonen av inputen
                pri_nåværende = pri_mønster[sekvens]

                # Pulsbredden defineres av pri og duty cycle
                puls_bredde = pri_nåværende * bølge_variabler.duty_cycle  # Beregn pulsbredden

                # Startindeks settes til start tiden multiplisert med samplingsfrekvens, for å få et faktisk samplingspunkt
                start_idx = int(start_tid * bølge_variabler.samplingsfrekvens) 

                # Sluttindeks settes til start tid + en pulsbredde, og her igjen mulitiplisert med samplingsfrekvensen
                slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens)  

                # Her lages faktisk selve pulsen, ved at den settes til 1 mellom start og slutt for en puls
                firkantpuls[start_idx:slutt_idx] = 1  

                # Lager et nytt startpunkt
                start_tid += pri_nåværende 

    # Firkantpuls som defineres dersom det skal være cw. Dette er egenltig bare en tidsvektor som er satt til 1 for alle verdier
    elif bølge_variabler.pri_mønster == 'cw':
        firkantpuls = np.ones_like(tidsvektor)
    
    # Firkantpuls som defineres for pausefunksjoner. Som forrige funksjon bare med null
    elif bølge_variabler.pri_mønster == 'pause':
        # Skriver 0 til hele firkantpulsen
        firkantpuls = np.zeros_like(tidsvektor) 

    # En helt standard firkantpuls dersom ingen PRI modulering ikke er angitt. Da antas fixed
    else:
        # Lager en tidsvektor
        tidsvektor = np.linspace(0, bølge_variabler.total_tid, int(bølge_variabler.samplingsfrekvens * bølge_variabler.total_tid), endpoint=False)
        
        # Initierer firkantpuls
        firkantpuls = np.zeros_like(tidsvektor)

        # Pulsbredden defineres av pri og duty cycle
        puls_bredde = bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.duty_cycle  # Beregn pulsbredden

        # Passer på at pulsen ikke begynner på 0
        start_tid = tidsvektor[1]

        for repetisjoner in range (bølge_variabler.repetisjoner):
            
            # Startindeks settes til start tiden multiplisert med samplingsfrekvens, for å få et faktisk samplingspunkt
            start_idx = int(start_tid * bølge_variabler.samplingsfrekvens) 

            # Sluttindeks settes til start tid + en pulsbredde, og her igjen mulitiplisert med samplingsfrekvensen
            slutt_idx = int((start_tid + puls_bredde) * bølge_variabler.samplingsfrekvens)  

            # Her lages faktisk selve pulsen, ved at den settes til 1 mellom start og slutt for en puls
            firkantpuls[start_idx:slutt_idx] = 1  

            # Lager et nytt startpunkt
            start_tid += bølge_variabler.pulsrepetisjonsintervall
    return firkantpuls


# Funksjon som genererer en sinus bølge 
def sinusbølge(bølge_variabler):

    # Definerer tidsvektor
    tidsvektor = np.arange(0, bølge_variabler.total_tid, 1 / bølge_variabler.samplingsfrekvens)

    # Definerer lengden på en pulsbredde
    sinus_varighet = bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.duty_cycle

    # Initier sinusbølgen, I bølgen, og Q bølgen
    sinus_bølge = np.zeros_like(tidsvektor)
    I_signal = np.zeros_like(tidsvektor)
    Q_signal = np.zeros_like(tidsvektor)

    # Sinusbølge, I bølge og Q bølge som lages dersom continuous wave er valgt
    if bølge_variabler.pri_mønster == 'cw':
        fase = 2 * np.pi * bølge_variabler.signalfrekvens * tidsvektor
        sinus_bølge = bølge_variabler.amplitude * np.sin(fase)
        # Faseforskyver I og Q signalene noe, for å få det rekonsturerte signalet til å begynne på riktig måte
        I_signal =    bølge_variabler.amplitude * np.cos(fase - np.pi/4)
        Q_signal =    bølge_variabler.amplitude * np.sin(fase - np.pi/4)
        
    if bølge_variabler.pri_mønster == 'pause':
        pass

    # Finn starten av hver firkantpuls-syklus (de tidene hvor firkantbølgen går fra 0 til 1)
    syklus_starter = np.where(np.diff((bølge_variabler.firkant_puls != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer sinus, Ibølge, Qbølge som starter på nytt. (Hver gang firkatnpulsen går fra 0 til 1)
    for start in syklus_starter:
        
        # Slutt er det samme som start + varigheten på pulsen. Må gange med samplingsfrekvens for å få det riktig
        slutt = start + int(sinus_varighet * bølge_variabler.samplingsfrekvens) 
        
        # Sørger for at vi ikke går utenfor tidsaksen
        slutt = min(slutt, len(tidsvektor))  

        # Beregn tidsvinduet for sinus innenfor denne syklusen. Kan da være synkronisert ved usynkrone pulser
        lokal_tid = tidsvektor[start:slutt] - tidsvektor[start]  

        #  Lager bølgene i en gitt tidsperiode
        fase = 2 * np.pi * bølge_variabler.signalfrekvens * lokal_tid
        sinus_bølge[start:slutt] = bølge_variabler.amplitude * np.sin(fase)
        # Faseforskyver I og Q signalene noe for at det rekonstruerte signalet skal begynne på riktig tidspunkt
        I_signal[start:slutt] =    bølge_variabler.amplitude * np.cos(fase - np.pi/4)
        Q_signal[start:slutt] =    bølge_variabler.amplitude * np.sin(fase - np.pi/4)
        
    return sinus_bølge, I_signal, Q_signal


# Funksjon som genrer en chirp bølge
def chirpbølge(bølge_variabler):
    # Definerer en startfrekvens
    start_frekvens = bølge_variabler.signalfrekvens  
    # Definerer en sluttfrekvens
    # Her vil det være mulig å endre slik at sluttfrekvensen kan justeres på av en bruker
    slutt_frekvens = bølge_variabler.signalfrekvens * 10  # Sluttfrekvens
    
    # Pulsbreddetid defineres
    chirp_varighet = bølge_variabler.pulsrepetisjonsintervall * bølge_variabler.duty_cycle

    # Tidsvektor defineres
    tidsvektor = np.arange(0, bølge_variabler.total_tid, 1 / bølge_variabler.samplingsfrekvens)

    # Initier chirp-signalet og IQ-signaler
    chirp_bølge = np.zeros_like(tidsvektor)
    I_signal = np.zeros_like(tidsvektor)
    Q_signal = np.zeros_like(tidsvektor)

    # Finn starten av hver firkantpuls-syklus
    syklus_starter = np.where(np.diff((bølge_variabler.firkant_puls != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer chirp
    for start in syklus_starter:
        # Beregner punkt for slutt. Slutt er start + varigheten til en puls
        slutt = start + int(chirp_varighet * bølge_variabler.samplingsfrekvens)  
        
        # Sørger for at programmet holder seg innenfor tidsaksen
        slutt = min(slutt, len(tidsvektor)) 
        
        # Lokal tidsvektor for chirp innenfor nåværende puls
        lokal_tid = np.linspace(0, chirp_varighet, slutt - start, endpoint=False)
        
        # Beregn faser ved å integrere frekvensen (fase = 2 pi * integral av frekvens)
        fase = 2 * np.pi * (start_frekvens * lokal_tid + (slutt_frekvens - start_frekvens) / (2 * chirp_varighet) * lokal_tid**2) 

        # Generer I- og Q-signaler med korrekt chirp-frekvens. (frekvensen endres lineært fra start til slutt)
        I_signal[start:slutt] = bølge_variabler.amplitude * np.cos(fase + np.pi / 4)
        Q_signal[start:slutt] = bølge_variabler.amplitude * np.sin(fase + np.pi / 4)

        # Generer selve chirp-bølgen (kan være lik I eller en annen definisjon)
        chirp_bølge[start:slutt] = bølge_variabler.amplitude * chirp(lokal_tid, start_frekvens, chirp_varighet, slutt_frekvens, method="linear")


    return chirp_bølge, I_signal, Q_signal


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
    barker_bølge_sekvens = np.zeros_like(tidsvektor)
    barker_bølge_endelig = np.zeros_like(tidsvektor)
    I_signal = np.zeros_like(tidsvektor)
    Q_signal = np.zeros_like(tidsvektor) 

    # Finn starten av hver firkantpuls-syklus. Firkantpulsen starter, eller er "på" når den ikke er 0
    syklus_starter = np.where(np.diff((bølge_variabler.firkant_puls != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer Barker-sekvensen. Når firkantpulsen går fra 0 til 1
    for start in syklus_starter:
        slutt = start + int(barker_varighet * bølge_variabler.samplingsfrekvens) # Slutt er start pluss varigheten med sampingsfekvensen
        slutt = min(slutt, len(tidsvektor))  # Sørg for at vi ikke går utenfor tidsaksen

        # Beregn antall samples per Barker-bit
        samples_per_bit = (slutt - start) // bølge_variabler.n_barker

        # Generer Barker-sekvens i dette tidsvinduet
        # Henter ut plassering og verdi fra barker sekvensen i 'i' og bit
        for i, bit in enumerate(barker_sekvens): 
            
             # Definerer en start avhengig av varigheten fra tideligere bits
            bit_start = start + i * samples_per_bit
            
            # Beregner avsluttende tid og forsikrer om at tiden ikke passerer 'slutt' slik at vektoren blir for lang
            bit_slutt = min(bit_start + samples_per_bit, slutt) 
            
            # Dette fyller en periode i barker sekvensen med en bit. Enten +1 eller -1
            barker_bølge_sekvens[bit_start:bit_slutt] = bit

        # Definerer fase
        fase = 2 * np.pi * bølge_variabler.signalfrekvens * (tidsvektor[start:slutt] - tidsvektor[start])
        
        # Generer lokal sinusbølge som starter på nytt for hver firkantpuls-syklus
        lokal_sinus_bølge = np.sin(fase)  

        # Multipliserer barker sekvensen med den lokale sinusbølgen for å modulere den. Det samme gjøres for I og Q signalene
        barker_bølge_endelig[start:slutt] = barker_bølge_sekvens[start:slutt] * lokal_sinus_bølge * bølge_variabler.amplitude
        I_signal[start:slutt] = barker_bølge_sekvens[start:slutt] * np.cos(fase - np.pi /4) * bølge_variabler.amplitude 
        Q_signal[start:slutt] = barker_bølge_sekvens[start:slutt] * np.sin(fase - np.pi /4) * bølge_variabler.amplitude
        
    return barker_bølge_endelig, I_signal, Q_signal


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
    # Hvis ikke dette er valgt, er det en ugyldig puls type, og programmet avsluttes
        raise ValueError("Ugyldig puls type")
    return endelig_bølge_valg
