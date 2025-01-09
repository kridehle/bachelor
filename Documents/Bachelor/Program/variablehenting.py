
def les_fra_fil():
    # Program to read the entire file using read() function
    file = open("variabler.txt", "r")
    content = file.read()
    print(content)
    file.close()
    return content

def hent_ut_variabler():
    
    print()



les_fra_fil()