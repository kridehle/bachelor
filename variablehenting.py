import ast


def les_fra_fil():
    # Program to read the entire file using read() function
    file = open("variabler.txt", "r")
    content = file.read()
    file.close()
    content = content.splitlines()
    return content

def hent_ut_variabler():
    values = {}
    content = les_fra_fil()

    for line in content:

        line = line.split("#", 1)[0].strip()

        if not line:
            continue

        line = line.strip()
        if "=" in line:
            name, value = line.split("=",1)
            name = name.strip()
            value = value.strip()
            try:
                value = eval(value)
            except:
                pass
            values[name] = value

    print(values)
