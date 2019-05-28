## Takes a directory of wavs, exports a directory of spectrograms (as png) 

import sys, os
import numpy as np
import scipy.io.wavfile as wf
from scipy.signal import spectrogram
from matplotlib import pyplot as plt

## SPECTOGRAM PARAMETERS ##

def get_wav_info(wav_file):
    frames, data = wf.read(wav_file)
    if len(np.shape(data)) == 2:
        info = data[:,0]
    else:
        info = data
    return info, frames

def wav_to_spect(wav_file):
    info, frames = get_wav_info(wav_file)
    f,t,Sxx = spectrogram(info, frames)
    Sxx = np.flipud(Sxx)
    return Sxx

def wav_to_png(wav_file):
    wav_name = wav_file.split('/')[-1]
    png_file = wav_name.split('.')[0] + '.png'
    Sxx = wav_to_spect(wav_file)
    plt.imsave(spect_dir + '/' + png_file,Sxx)

if __name__ == '__main__':
    wav_dir = sys.argv[1]
    spect_dir = sys.argv[2]

    wav_dir = os.path.abspath(wav_dir)
    spect_dir = os.path.abspath(spect_dir)

    for wav in os.listdir(wav_dir):
        if '.wav' not in wav:
            continue
        else:
            wav_to_png(wav_dir + '/' + wav)

    print('All done!')
