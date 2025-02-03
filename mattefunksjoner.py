import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square
from scipy.signal import chirp


"""Globale varibler er: fs: samplingsfrekvens f: signalfrekvens pri: pulse_repetition_interval prf: pulse_repetition_frequency dc: duty_cycle t: tid/varighet n: sekvens_til_barker m: pri_mønster r: repetisjoenr"""
def globale_variabler(fs_i, f_i, pri_i, prf_i, dc_i, t_i, n_i, m_i, r_i):
    # Definerer globale variabler som kommer til å bli brukt gjennom hele programmet
    global fs, f, pri, prf, dc, t, n, m, r, f_firkant, pwt, t_tot, hvile_før_start
    
    # Tildeler de globale variablene verdier definert av brukeren eller forhåndsdefinerte
    fs, f, pri, prf, dc, t, n, m, r = fs_i, f_i, pri_i, prf_i, dc_i, t_i, n_i, m_i, r_i
   
    # Hvis hverken PRI/PRF er definert, tildeles PRI en verdi fra frekvensen til signalet.
    if pri == 0 and prf == 0:
        pri = (1/f) * 10
        print(f"PRI/PRF ikke angitt. PRI settes til {pri}")

    # Hvis pri ikke er angitt, får pri verdien til prf
    if pri == 0:
        try:
            pri = 1 / prf
        except ZeroDivisionError:
            print(f"prf kan ikke være {prf}")
            
    # Definerer tiden for en firkantpuls
    f_firkant = 1 / pri
    # Definerer tiden det tar for en pulsbredde og printer den
    pwt = pri * dc
    print(f"Puls bredde tid er {pwt}")
    
    # Hvis det er satt et antall repetisjoner, defineres tiden av pri og antall repetisjoner
    if r != 0:
        t_i = (pri * r) + pri
    
    # Definerer en total tid, basert på inputtid. Inputtiden er enten definert av variabler, eller av pri og antall repetisjoner. 
    t_tot = t_i
    # Definerer en felles tidsvektor
    t = np.arange(0, t_i, 1 / fs)
    # Definerer en hvile før start tid, slik at det ikke skal komme for mange jitter signal
    hvile_før_start = pri * 0.5


# Funksjon som lager en sinusbølge. Sinusbølgen følger firkantpulsen. For at dette sakl fungere under jitter/stagger er denne funksjonen litt komplisert
def sinus_bølge():
    firkant_bølge = firkantpuls()  # Hent firkantpulsen for å styre aktivering
    sinus_varighet = pwt  # Varigheten er det samme som tiden til en pulsbredde

    # Initier sinusbølgen
    sinus_bølge = np.zeros_like(t)

    # Finn starten av hver firkantpuls-syklus (de tidene hvor firkantbølgen går fra 0 til 1)
    syklus_starter = np.where(np.diff((firkant_bølge != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer sinus som starter på nytt
    for start in syklus_starter:
        slutt = start + int(sinus_varighet * fs)
        slutt = min(slutt, len(t))  # Sørg for at vi ikke går utenfor tidsaksen

        # Beregn tidsvinduet for sinus innenfor denne syklusen
        lokal_t = t[start:slutt] - t[start]  # Juster for å starte på 0
        sinus_bølge[start:slutt] = np.sin(2 * np.pi * f * lokal_t)

    return sinus_bølge


# Funksjon som genererer en firkantpuls. Frekvens og duty cycle defineres av variablene i inputen. Hvis ingen 
# ønskede verdier er gitt, settes det forhåndsdefinerte verdier.
def firkantpuls():  
    if m == 'jitter':
        # Beregn perioden og pulsbredden
        jitter_prosent = 0.1    
        
        periode = 1 / f_firkant
        puls_bredde = dc * periode

        # Generer tidsvektor
        t_lokal = np.linspace(0, t_tot, int(fs * t_tot), endpoint=False)

        # Start- og sluttidspunkter for hver puls med jitter
        start_tider = np.arange(0, t_tot, periode)
        jitter = np.random.uniform(-jitter_prosent * periode, jitter_prosent * periode, size=len(start_tider))
        start_tider_jittered = start_tider + jitter

        # Generer firkantpuls
        firkantpuls = np.zeros_like(t_lokal)
        for start_tid in start_tider_jittered:
            start_idx = int(start_tid * fs)
            slutt_idx = int((start_tid + puls_bredde) * fs)
            if start_idx < len(t_lokal):
                firkantpuls[start_idx:slutt_idx] = 1

        # Sett firkantpulsen til 0 frem til hviletiden
        firkantpuls[t_lokal < hvile_før_start] = 0

    else:
        t = np.linspace(0, t_tot, int(fs * t_tot), endpoint=False)
        firkantpuls = (square(2 * np.pi * f_firkant * t, duty=dc) + 1) / 2
        firkantpuls[t < hvile_før_start] = 0

    return firkantpuls


# Funksjon for en pulskodet bølge. Chirp bølge
def chirp_bølge():
    f0 = f #Frekvensen f0 er startfrekvesn
    f1 = 10*f #Frekvensen f1 er sluttfrekvens
    firkant_bølge = firkantpuls() #Henter inn firkantbølge for å kunne sende chirp i pulser
    chirp_varighet = pwt #Varigheten er det samme som tiden til en pulsbredde
    
    # Initier chirp-signalet
    ch_bølge = np.zeros_like(t)

    # Finn starten av hver firkantpuls-syklus
    syklus_starter = np.where(np.diff((firkant_bølge != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer chirp
    for start in syklus_starter:
        slutt = start + int(chirp_varighet * fs)
        slutt = min(slutt, len(t))  # Sørg for at vi ikke går utenfor tidsaksen
        # Beregn tidsvinduet for chirp innenfor denne syklusen
        ch_bølge[start:slutt] = chirp(
            t[:slutt - start], f0, chirp_varighet, f1, method="linear"
        )

    return ch_bølge


# Funksjon som inneholder forskjellige barker sekvenser
def barker_kode(n):
    barker_sekvens = {
        2: [1, -1],
        3: [1, 1, -1],
        4: [1, 1, -1, 1],
        5: [1, 1, 1, -1, 1],
        7: [1, 1, 1, -1, -1, 1, -1],
        11: [1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1],
        13: [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1]
    }
    
    if n not in barker_sekvens:
        raise ValueError(f"Barker kode med lengde {n} finnes ikke. Verdien må være 2,3,4,5,7,11 eller 13")
    return barker_sekvens[n]


def barker_bølge():
    barker_sekvens = barker_kode(n)  # Hent Barker-koden og lagrer en variant av den
    firkant_bølge = firkantpuls()  # Hent firkantpulsen for å styre aktivering
    barker_varighet = pwt  # Varigheten til en Barker-sekvens er lik en pulsbredde
                           # Samme tankegang som med Chirp
                           
    # Initier Barker-signalet
    barker_bølge = np.zeros_like(t)

    # Finn starten av hver firkantpuls-syklus. Firkantpulsen starter, eller er "på" når den ikke er 0
    syklus_starter = np.where(np.diff((firkant_bølge != 0).astype(int)) == 1)[0] + 1

    # Iterer over hver syklus og generer Barker-sekvensen
    for start in syklus_starter:
        slutt = start + int(barker_varighet * fs)
        slutt = min(slutt, len(t))  # Sørg for at vi ikke går utenfor tidsaksen

        # Beregn antall samples per Barker-bit
        samples_per_bit = (slutt - start) // n

        # Generer Barker-sekvens i dette tidsvinduet
        for i, bit in enumerate(barker_sekvens):
            bit_start = start + i * samples_per_bit
            bit_slutt = min(bit_start + samples_per_bit, slutt)
            barker_bølge[bit_start:bit_slutt] = bit

        # Generer lokal sinusbølge som starter på nytt for hver firkantpuls-syklus
        lokal_sinus_bølge = np.sin(2 * np.pi * f * (t[start:slutt] - t[start]))  # Tidsforskyvning for synkronisering

        # Multiplicer barker_bølge med den lokale sinusbølgen
        barker_bølge[start:slutt] = barker_bølge[start:slutt] * lokal_sinus_bølge

    return barker_bølge


#Funksjon som plotter resultatet
def plott_resultat(final_wave):
    # Plot the result

    plt.figure(figsize=(10, 4))
    plt.plot(t, final_wave, label=f"(f={f} Hz, fs={fs:.1f} Hz)",color = 'b')
    plt.title("Visuell plot")
    plt.xlabel("Tid (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.savefig('output.png')
    plt.close()
