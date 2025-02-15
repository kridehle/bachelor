import sys
import numpy as np

objekter = []

class BølgeVariabler:

    def __init__(self, signalfrekvens, samplingsfrekvens, pulsrepetisjonsintervall, duty_cycle, puls_type, n_barker, mønster, repetisjoner, stagger_verdier, total_tid, firkant_puls, endelig_bølge):
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

    def verifiser_variabler(self):
        print(f"Signalfrekvens: {self.signalfrekvens} Hz\nSamplingsfrekvens: {self.samplingsfrekvens} Hz\nPulsrepetisjonsintervall: {self.pulsrepetisjonsintervall} s\nDuty cycle: {self.duty_cycle}\nPuls type: {self.puls_type}\nBarker sekvens: {self.n_barker}\nPulsmønster: {self.pri_mønster}\nRepetisjoner: {self.repetisjoner}\nStagger verdier: {self.stagger_verdier}\n")


def les_fil(filnavn):
    # Åpner en fil og leser linjene
    data = '' # Initierer en tom streng
    with open(filnavn, "r", encoding="utf-8") as fil:
        data = fil.read()
        data = '\n'.join([linje.split('#', 1)[0].strip() for linje in data.splitlines()])
    
    linjer = [linje.strip() for linje in data.split("\n") if linje.strip()]

    return linjer

def liste_til_ordbok(input_liste):
    deler = input_liste.split()
    if len(deler) % 2 != 0:
        raise ValueError("Listen må ha et partall antall elementer")
    
    variabler = {deler[i]: deler[i + 1] for i in range(0, len(deler), 2)}
    return variabler



def henter_variabler():
    input = les_fil('variabler.txt')

    for n in range(len(input)):

        lokal_input = liste_til_ordbok(input[n])

        standard_signalfrekvens = 1000
        
        standard_pulsrepetisjonsintervall = 0.1
        standard_duty_cycle = 0.1
        standard_puls_type = 'ukodet'
        standard_n_barker = 2
        standard_mønster = 'ukodet'
        standard_repetisjoner = 1
        standard_stagger_verdier = 0


        signalfrekvens = float(lokal_input.get('f', standard_signalfrekvens))

        standard_samplingsfrekvens = 1000 * signalfrekvens

        samplingsfrekvens = float(lokal_input.get('fs', standard_samplingsfrekvens))
        pulsrepetisjonsintervall = float(lokal_input.get('pri', standard_pulsrepetisjonsintervall))
        duty_cycle = float(lokal_input.get('dc', standard_duty_cycle))
        puls_type = lokal_input.get('pt', standard_puls_type)
        n_barker = int(lokal_input.get('n', standard_n_barker))
        mønster = lokal_input.get('pm', standard_mønster)
        repetisjoner = int(lokal_input.get('r', standard_repetisjoner))
        
        
        deler = mønster.split(',')
        mønster = deler [0]
        stagger_verdier = deler[1:]
        stagger_verdier = list(map(float, stagger_verdier))

        total_tid = np.array([])
        firkant_puls = np.array([])
        endelig_bølge = np.array([])


        objekter.append(BølgeVariabler(signalfrekvens, samplingsfrekvens,
                                        pulsrepetisjonsintervall, duty_cycle,
                                          puls_type, n_barker, mønster, repetisjoner,
                                            stagger_verdier, total_tid, firkant_puls,
                                            endelig_bølge))
    return objekter
