import numpy as np
import argparse

objekter = []

# Definerer en klasse som kalles for BølgeVariabler. Objekter av denne klassen er selve ryggmargen til programmet
class BølgeVariabler:

    # Verdier som finnes i klassen BølgeVariabler. Hvert eneste objekt inneholder all denne informasjonen
    def __init__(self, signalfrekvens, samplingsfrekvens, pulsrepetisjonsintervall, duty_cycle, puls_type, n_barker, mønster, repetisjoner, stagger_verdier, total_tid, firkant_puls, endelig_bølge, amplitude, dwell_verdier, dwell_repetisjoner):
        self.signalfrekvens = signalfrekvens
        self.samplingsfrekvens = samplingsfrekvens
        self.pulsrepetisjonsintervall = pulsrepetisjonsintervall
        self.duty_cycle = duty_cycle
        self.puls_type = puls_type
        self.n_barker = n_barker
        self.pri_mønster = mønster
        self.repetisjoner = repetisjoner
        self.stagger_verdier = stagger_verdier
        self.total_tid = total_tid
        self.firkant_puls = firkant_puls
        self.endelig_bølge = endelig_bølge
        self.amplitude = amplitude
        self.dwell_verdier = dwell_verdier
        self.dwell_repetisjoner = dwell_repetisjoner

    # Funksjon som gjør at en bruker visuelt kan verifisere variablene til et gitt objekt. Er så enkelt at variabeltype og verdi printes
    def verifiser_variabler(self):
        print(f"Signalfrekvens: {self.signalfrekvens} MHz\nSamplingsfrekvens: {self.samplingsfrekvens} MHz\nPulsrepetisjonsintervall: {self.pulsrepetisjonsintervall} us\nAmplitude: {self.amplitude}\nDuty cycle: {self.duty_cycle * 100} %\nPuls type: {self.puls_type}\nBarker sekvens: {self.n_barker}\nPulsmønster: {self.pri_mønster}\nRepetisjoner: {self.repetisjoner}\nStagger verdier: {self.stagger_verdier} us\nDwell verdier: {self.dwell_verdier} us\nDwell repetisjoner: {self.dwell_repetisjoner}\n")

# Funksjon som leser en fil og separerer forskjellige linjer i filen. 
# Dersom den finner en '#' tolkes dette som en kommentar og alt bak en '#' dumpes
def les_fil(filnavn):
    # Initierer en tom streng
    data = '' 
    # Åpner en fil og leser len linje
    with open(filnavn, "r", encoding="utf-8") as fil:
        # Leser filen
        data = fil.read()
        # Fjerner alt som finnes bak '#'
        data = '\n'.join([linje.split('#', 1)[0].strip() for linje in data.splitlines()])
    # Splitter linjer ved linjeskift og fjerner tomme linjer
    linjer = [linje.strip() for linje in data.split("\n") if linje.strip()]

    return linjer

# Lager en ordbok av streng input
def liste_til_ordbok(input_liste):
    # Initierer deler som inneholder forskjellige strenger
    deler = input_liste.split()
    # Sjekker antall objekter i deler. Dersom ikke 2 er inputen feil, og programmet slutter
    if len(deler) % 2 != 0:
        raise ValueError("Listen må ha et partall antall elementer")
    
    # Lager en ordbok som består av variabel og verdi
    variabler = {deler[i]: deler[i + 1] for i in range(0, len(deler), 2)}

    # Returnerer ordboken
    return variabler

# Funksjon som henter variabler og tildeler standard verdier
def henter_variabler():
    # Benytter seg av les fil og lagrer dette som input
    
    args = kommandolinje_argumenter()
    
    filnavn = args.fil if args.fil else "variabler.txt"
    
    input = les_fil(filnavn)

    # Lager en løkke som itererer over antall linjer
    for n in range(len(input)):

        # Lager en liste per linje
        lokal_input = liste_til_ordbok(input[n])

        # Definerer standard variabler
        standard_signalfrekvens = 1
        standard_samplingsfrekvens = 61.44
        standard_pulsrepetisjonsintervall = 0.1
        standard_duty_cycle = 0.1
        standard_puls_type = 'ukodet'
        standard_n_barker = 2
        standard_mønster = 'ukodet'
        standard_repetisjoner = 1
        standard_amplitude = 1
        
        if args.samplingsfrekvens:
            samplingsfrekvens = args.samplingsfrekvens

        # Henter signalfrekvens, hvis ikke får den standard verdi
        signalfrekvens = float(lokal_input.get('f', standard_signalfrekvens))

        # Henter pulsrepetisjonsintervall, hvis ikke får PRI standard verdi
        pulsrepetisjonsintervall = float(lokal_input.get('pri', standard_pulsrepetisjonsintervall))
        
        # Henter duty cycle, hvis ikke får den standard verdi
        duty_cycle = float(lokal_input.get('dc', standard_duty_cycle))

        # Henter puls type, hvis ikke får den standard verdi
        puls_type = lokal_input.get('pt', standard_puls_type)

        # Henter ønsket barker sekvens, hvis ikke settes den til en standard verdi
        n_barker = int(lokal_input.get('n', standard_n_barker))

        # Henter pulsmønster, hvis ikke settes det til standard mønster ukodet
        mønster = lokal_input.get('pm', standard_mønster)

        # Henter repetisjoner, hvis ikke settes det til 1
        repetisjoner = int(lokal_input.get('r', standard_repetisjoner))

        # Henter amplitude, hvis ikke settes den til 1
        amplitude = float(lokal_input.get('a', standard_amplitude))
        
        # Denne er til stagger. Skiller staggerdefinisjon og verdier med ','
        deler = mønster.split(',')
        # Mønster får den første delen 
        mønster = deler [0]
        # Stagger verdier får alle verdiene etter den første verdien
        
        stagger_verdier = []
        dwell_verdier = []
        dwell_repetisjoner = []
        
        if mønster == 'stagger':
            stagger_verdier = deler[1:]
            # Stagger verdier lagres som floats
            stagger_verdier = list(map(float, stagger_verdier))
            
        if mønster == 'dwell':    
            # Dwell verider er annenhver av delene, og begynner på 1
            dwell_verdier = deler[1::2]
            # Gjør dwell verdier til floats
            dwell_verdier = list(map(float, dwell_verdier))
            # Dwell repetisjoner er annenhver av delene, og begynner på 2
            dwell_repetisjoner = deler [2::2]
            # Gjør dwell repetisjoner til ints
            dwell_repetisjoner = list(map(int, dwell_repetisjoner))

        # Initierer total tid
        total_tid = np.array([])

        # Initierer firkantpuls
        firkant_puls = np.array([])

        # Initierer endelig bølge
        endelig_bølge = np.array([])

        # Legger til verdiene til ett objekt i bølgevariabler.
        objekter.append(BølgeVariabler(signalfrekvens, samplingsfrekvens,
                                        pulsrepetisjonsintervall, duty_cycle,
                                          puls_type, n_barker, mønster, repetisjoner,
                                            stagger_verdier, total_tid, firkant_puls,
                                            endelig_bølge, amplitude, dwell_verdier, dwell_repetisjoner))
    return objekter,args

# Funksjon som henter og verifiserer variabler. Debbe kalles opp av main
def hent_og_verifiser_variabler():
    # Administrativ teller for å gjøre det lett forståelig for en bruker
    teller = 1
    # Henter variabler
    bølge_variabler, args = henter_variabler()
    # Itererer gjennom alle objektene
    for n in bølge_variabler:
        # Gjør det mulig for en bruker å lese gjennom å validere alle variablene
        print(f"\nDette er bølge variablene for bølge nummer: {teller}")
        BølgeVariabler.verifiser_variabler(n)

        teller += 1
    return bølge_variabler, args

def kommandolinje_argumenter():
    parser = argparse.ArgumentParser(description="henter argumenter fra kommandolinjen")
    
    # Legg til argumentene
    parser.add_argument("-f", "--fil", type = str, help = "filnavn, eller sti til filen")
    parser.add_argument("-fs", "--samplingsfrekvens", type = float, help = "samplingsfrekvens til signalet")
    parser.add_argument("-dt", "--datatype", type = str, help = "ønsket datatype. kan vlege mellom f (32bit float) og i (16 bit int)")
    
    # Parser argumentene
    args = parser.parse_args()
    
    return args