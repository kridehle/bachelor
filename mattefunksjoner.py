import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

duration = 0.1  # Total duration of the signal (seconds)

def sine_wave(fs, f):
    # Define the time vector
    global t
    t = np.arange(0, duration, 1 / fs)

    # Generate the sine wave
    sine_wave = np.sin(2 * np.pi * f * t)

    return sine_wave

def square_wave(fs,f,pri,prf,duty_cycle):  
    global t
    t = np.arange(0, duration, 1 / fs)
    
      
    # Generate square wave
    if pri == 0:
        frequency_square = prf  # frequency (Hz)
    elif prf == 0:
        frequency_square = 1/pri
    else:
        print("PRI/PRF ikke angitt. Setter PRF = f/10")
        frequency_square = f/10
    if duty_cycle == 0:
        print("Dutycycle ikke satt. Settes til 0.01")
        duty_cycle = 0.01  # percentage of the period where the signal is high
    square_wave = (square(2 * np.pi * frequency_square * t, duty=duty_cycle)+1)/2
    return square_wave

    
def plot_result(final_wave,f,fs):
    # Plot the result
    plt.figure(figsize=(10, 4))
    plt.plot(t, final_wave, label=f"Sine wave modulated by square wave (f={f} Hz, fs={fs:.1f} Hz)")
    plt.title("Sine Wave Modulated by Square Wave")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.show()

