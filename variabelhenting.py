import sys

class BølgeVariabler:
    def __init__(self, signalfrekvens, samplingsfrekvens, pulsrepetisjonsintervall, duty_cycle, tid, puls_type, n_barker, mønster, repetisjoner, stagger_verdier):
        self.signalfrekvens = signalfrekvens
        self.samplingsfrekvens = samplingsfrekvens
        self.pulsrepetisjonsintervall = pulsrepetisjonsintervall
        self.duty_cycle = duty_cycle
        self.tid = tid
        self.puls_type = puls_type
        self.n_barker = n_barker
        self.pri_mønster = mønster
        self.repetisjoner = repetisjoner
        self.stagger_verdier = stagger_verdier

    def verifiser_variabler(self):
        print(f"Signalfrekvens: {self.signalfrekvens} Hz\nSamplingsfrekvens: {self.samplingsfrekvens} Hz\nPulsrepetisjonsintervall: {self.pulsrepetisjonsintervall} s\nDuty cycle: {self.duty_cycle}\nTid: {self.tid} s\nPuls type: {self.puls_type}\nN til barker: {self.n_barker}\nPulsmønster: {self.pri_mønster}\nRepetisjoner: {self.repetisjoner}\nStagger verdier: {self.stagger_verdier}")

def standard_variabler():
    signalfrekvens = 1000
    samplingsfrekvens = 8000 * signalfrekvens
    pulsrepetisjonsintervall = 0.1
    duty_cycle = 0.1
    tid = 1
    puls_type = 'ukodet'
    n_barker = 2
    mønster = 'ukodet'
    repetisjoner = 2
    stagger_verdier = 0

    bølge = BølgeVariabler(signalfrekvens, samplingsfrekvens, pulsrepetisjonsintervall, duty_cycle, tid, puls_type, n_barker, mønster, repetisjoner, stagger_verdier)
    return bølge

def les_fil(filnavn):
    # Åpner en fil og leser linjene
    data = '' # Initierer en tom streng
    with open(filnavn, "r", encoding="utf-8") as fil:
        data = fil.read()
        data = '\n'.join([linje.split('#', 1)[0].strip() for linje in data.splitlines()])
    
    linjer = [linje.strip() for linje in data.split("\n") if linje.strip()]

    return linjer

def henter_variabler():
    input = les_fil('variabler.txt')
    print(input)
    print(len(input))
    objekt = []

    for n in range(len(input)):

        lokal_input = input[n].split()

        print(lokal_input)

        signalfrekvens = lokal_input.get('f')
        samplingsfrekvens = lokal_input.get('fs')
        pulsrepetisjonsintervall = lokal_input.get('pri')
        duty_cycle = lokal_input.get('dc')
        tid = lokal_input.get('t')
        puls_type = lokal_input.get('pt')
        n_barker = lokal_input.get('n')
        mønster = lokal_input.get('pm')
        repetisjoner = lokal_input.get('r')
        stagger_verdier = lokal_input.get('sv')


        objekt[n] = BølgeVariabler(signalfrekvens, samplingsfrekvens, pulsrepetisjonsintervall, duty_cycle, tid, puls_type, n_barker, mønster, repetisjoner, stagger_verdier)
    return objekt

o = henter_variabler()
print (o)
