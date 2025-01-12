import variablehenting
import mattefunksjoner

def main():
    Fs,f,s = variablehenting.separer_variabler()    
    mattefunksjoner.signal(Fs,f,s)
  
if __name__ == "__main__":
    main()