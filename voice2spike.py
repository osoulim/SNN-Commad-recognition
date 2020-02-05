import sys
import cochlea3
from scipy.io import wavfile
import numpy as np
import scipy.signal as dsp 

def wave2spike(filename):
    fs, sound = wavfile.read(filename)
    print(fs, sound.shape)
    print(map(float, sound))

    fs = 100e3
    # t = np.arange(0, 0.1, 1/fs)
    # s = dsp.chirp(t, 80, t[-1], 20000)
    # s = cochlea3.set_dbspl(s, 50)
    # pad = np.zeros(int(10e-3 * fs))
    # sound = np.concatenate( (s, pad) )
    # print(fs, sound.shape)
    anf_trains = cochlea3.run_zilany2014(
        sound=sound.astype(float) / 10000,
        fs=fs,
        anf_num=(26, 0 , 0),
        cf=1000,
        species='human',
        seed=0
    )
    return anf_trains

if __name__ == "__main__":
    filename = sys.argv[1]
    print(wave2spike(filename))

