import sys
import cochlea3
from scipy.io import wavfile
import numpy as np
import scipy.signal as dsp 

def wave2spike(filename, anf_size):
    fs, sound = wavfile.read(filename)
    fs = 100e3
    anf_trains = cochlea3.run_zilany2014(
        sound=sound.astype(float) / 10000,
        fs=fs,
        anf_num=(anf_size, 0 , 0),
        cf=1000,
        species='human',
        seed=0
    )
    return anf_trains

if __name__ == "__main__":
    filename = sys.argv[1]
    print(wave2spike(filename))

