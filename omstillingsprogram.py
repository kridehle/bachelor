import variablehenting
import mattefunksjoner

def main():
    Fs,f,pri,prf,dc = variablehenting.separer_variabler()
    if Fs == 0:
        Fs = 20 * f  # Default sampling frequency    
    sine_wave = mattefunksjoner.sine_wave(Fs,f)
    square_wave = mattefunksjoner.square_wave(Fs,f,pri,prf,dc)
    result = sine_wave * square_wave
    mattefunksjoner.plot_result(result,f,Fs)


  
if __name__ == "__main__":
    main()