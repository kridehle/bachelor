# Bachelorprogram
Programmering til bachelor Kristoffer Dehle

## Viktig info

Det kommer til å ligge en versjonslogg i mappen(e) versjon_(X). Filene som ligger utenfor innholdet i en versjonsmappe er filer som har det nyeste innholdet. Dette innholdet testes, og det er ikke validert at noe av det faktisk fungerer som det burde gjøre. 

## Hvordan kjøre programmet?

For å kjøre programmet åpner man en terminal, og skriver inn ´python3 omstillingsprogram.py´

I forkant av dette er det lurt å ha endret på verdiene som ligger i tekstfilen variabler.

## Hvordan legge inn variabler?

Her er en oversikt over variablene man kan legge inn, og hvordan man gjør det. Merk, klammeparantesene er bare tilstede for å vise hva som hører til. Dersom du faktisk skal skrive inn verdier er ikke klammeparanteser nødvendig. Rekkefølgen på hvordan du skriver inn variablene er uvesentlig. En bølge defineres på en enkelt linje. Du kan legge til flere bølger etter hverandre med å skrive flere linjer med bølgevariabler under hverandre. Bølgene vil da bli produsert i rekkefølgen du har skrevet de opp i.

```
signalfrekvens: f [ønsket frekvens i Hz]

samplingsfrekvns: fs [ønsket samplingsfrekvens i Hz]

pulsrepetisjonsintervall: pri [ønsket pri]

antall repetisjoner: r [repetisjoner]

puls type/modulering: pt [ønsket pulstype]
  GODKJENTE PT VERDIER: ukodet, barker, chirp

PRI mønster: pm [ønsket primønster]
  GODKJENTE PM VERDIER: ukodet, jitter, stagger, dwell, pause, cw

  !NB! ved bruk av stagger:
    pm stagger,[pri 1],[pri 2],...,[pri n]
  !NB! ved bruk av dwell to dwell:
    pm dwell,[pri 1],[repetisjoner 1],pri[2],repetisjoner 2],...,...,[pri n],[repetisjoner n]
  !NB! lengden på en cw eller en pause er definert av pri!

ønsket barker sekvens: n [ønsket sekvens]
  
amplitude: a [ønsket amplitude]

dutycycle: dc [ønsket dutycycle]
```
