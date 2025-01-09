
def les_fra_fil():
    # Program to read the entire file using read() function
    file = open("variabler.txt", "r")
    content = file.read()
    file.close()
    return content

def hent_ut_variabler():
    values = {}
    content = les_fra_fil()
    #print(content)
    for line in content:
        line = line.strip()
        if "=" in line:
            name, value = line.split("=",1)
            name = line.strip()
            value = value.strip()
            try:
                value = eval(value)
            except:
                pass
            values[name] = value

    print(values)
