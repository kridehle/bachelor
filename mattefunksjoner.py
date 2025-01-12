import matplotlib.pyplot as plt
import numpy as np
from math import *

def signal(Fs, f, s):  
    x = np.arange(s/100)
    y = np.sin(2 * np.pi * f * x / Fs)
    plt.plot(x, y)
    plt.xlabel('sample(n)')
    plt.ylabel('magnitude')
    plt.show()

