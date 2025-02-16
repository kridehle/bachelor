import numpy as np

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
        print(f"Signalfrekvens: {self.signalfrekvens} Hz\nSamplingsfrekvens: {self.samplingsfrekvens} Hz\nPulsrepetisjonsintervall: {self.pulsrepetisjonsintervall} s\nAmplitude: {self.amplitude}\nDuty cycle: {self.duty_cycle}\nPuls type: {self.puls_type}\nBarker sekvens: {self.n_barker}\nPulsmønster: {self.pri_mønster}\nRepetisjoner: {self.repetisjoner}\nStagger verdier: {self.stagger_verdier}\nDwell verdier: {self.dwell_verdier}\nDwell repetisjoner: {self.dwell_repetisjoner}\n")

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
    input = les_fil('variabler.txt')

    # Lager en løkke som itererer over antall linjer
    for n in range(len(input)):

        # Lager en liste per linje
        lokal_input = liste_til_ordbok(input[n])

        # Definerer standard variabler
        standard_signalfrekvens = 1000
        standard_pulsrepetisjonsintervall = 0.1
        standard_duty_cycle = 0.1
        standard_puls_type = 'ukodet'
        standard_n_barker = 2
        standard_mønster = 'ukodet'
        standard_repetisjoner = 1
        standard_stagger_verdier = 0
        standard_amplitude = 1

        # Henter signalfrekvens, hvis ikke får den standard verdi
        signalfrekvens = float(lokal_input.get('f', standard_signalfrekvens))

        # Dene variablen er avhengig av standard frekvensen, så her settes den til 1000 signalfrekvens. Dette kan selvfølgelig endres
        standard_samplingsfrekvens = 1000 * signalfrekvens

        # Henter samplingsfrekvens, hvis ikke får den standard verdi
        samplingsfrekvens = float(lokal_input.get('fs', standard_samplingsfrekvens))

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
        stagger_verdier = deler[1:]
        # Stagger verdier lagres som floats
        stagger_verdier = list(map(float, stagger_verdier))
        
        dwell_verdier = deler[1::2]

        dwell_verdier = list(map(float, dwell_verdier))

        dwell_repetisjoner = deler [2::2]

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
    return objekter

# Funksjon som henter og verifiserer variabler. Debbe kalles opp av main
def hent_og_verifiser_variabler():
    # Administrativ teller for å gjøre det lett forståelig for en bruker
    teller = 1
    # Henter variabler
    bølge_variabler = henter_variabler()
    # Itererer gjennom alle objektene
    for n in bølge_variabler:
        # Gjør det mulig for en bruker å lese gjennom å validere alle variablene
        print(f"\n\nDette er bølge variablene for bølge nummer: {teller}")
        BølgeVariabler.verifiser_variabler(n)

        teller += 1
    return bølge_variabler