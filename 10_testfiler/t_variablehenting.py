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
            pass  # Hvis konverteringen feiler, behold verdien som en streng

        variabler[nøkkel] = verdi  # Legger til i dictionary

    return variabler


# Henter input fra filen
input_str = les_fil('t_variabler.txt')
resultat = behandle_input(input_str)

print(resultat)
