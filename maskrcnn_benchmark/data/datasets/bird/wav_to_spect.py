## Takes a directory of wavs, exports a directory of spectrograms (as png) 

import sys, os
import numpy as np
import scipy.io.wavfile as wf
from scipy.signal import spectrogram
from matplotlib import pyplot as plt
import pandas as pd

## Initialize these, just in case...

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
    f,ts,Sxx = spectrogram(info, frames)
    Sxx = np.flipud(Sxx)
    return f, ts, Sxx

def wav_to_png(wav_file, png_file = None, save=True):
    wav_name = wav_file.split('/')[-1]
    f,ts,Sxx = wav_to_spect(wav_file)
    if save:
        if png_file == None:
            png_file = wav_file + '.png'
        plt.imsave(png_file,Sxx)
    return f, ts, Sxx

## gets pixel (index) value from time (seconds). Needs pixels per second
def time_to_pixel(t_seconds, t0, t_res):
    t_wav = t_seconds - t0
    t_pixel = t_wav * t_res
    return int(np.floor(t_pixel))

## gets pixel (index) value from time (seconds).
def find_time(ts, t_start = 0, t_stop = -1):
    if t_start <= ts[0]: # Deal with edge case
        i_start = 0
    else:
        i_start = np.searchsorted(ts,t_start) - 1 
    i_stop = np.searchsorted(ts,t_stop) - 1
    return i_start, i_stop


## Takes annotation file of format: 
##   (wav_file_name,label start (sample), label finish (sample), label, tstart, tfinish, line #, wav #
## Returns pandas df of format
##   Name Boxes Labels
def parse_annotation(annot_file, sampling_rate = 48000):
## Read through file and shove the data into a couple lists and dicts
    with open(annot_file,'r') as annotations:
        boxes, labels = {},{}
        names = []
        for line in annotations:
            columns = line.split(',')
            line_id = int(columns[7])
            (chunk_name, sample_start, sample_end, label) = columns[0:4]
            sample_start = float(sample_start)
            sample_end = float(sample_end)
            if chunk_name not in names:
                names.append(chunk_name)
                boxes[chunk_name] = []
                labels[chunk_name] = []
            boxes[chunk_name].append([sample_start / sampling_rate, sample_end / sampling_rate])
            labels[chunk_name].append(label)
## Initialize pd dataframe
    data = {'Name':names,'Boxes_t':[[]] * len(names),'Boxes_i':[[]] * len(names),'Labels': [[]] * len(names)}
    annot_df = pd.DataFrame(data=data,columns=['Name','Boxes_t','Boxes_i','Labels']) 
    for i in range(len(names)):
        annot_df.loc[i]['Boxes_t'] = boxes[annot_df.loc[i]['Name']]
        annot_df.loc[i]['Labels'] = labels[annot_df.loc[i]['Name']]
    return annot_df

def make_annotation(wav_dir,annot_file, save=False,spect_dir = None):
    annot_df = parse_annotation(annot_file)
    wav_list = sorted(os.listdir(wav_dir))
    ## Step through each wav and update the annotation (save a spect while you're at it if you want.) 
    for wav in wav_list:
        if '.wav' not in wav:
            continue
        png_file = None
        if spect_dir != None:
            png_file = wav.split('.')[0] + '.png'
            png_file = spect_dir + '/' + png_file
        f, ts, Sxx = wav_to_png(wav_dir + '/' + wav, png_file,save=save)
        ## Sometimes pandas is stupid: this recovers the index for the row
        wav_index = annot_df.index[annot_df['Name'] == wav].tolist()[0]
        wav_annot = annot_df.loc[wav_index]
        ## Annoyingly, pandas treats .loc[int] differently from .loc[logical]
        labels = wav_annot['Labels']
        boxes_t = wav_annot['Boxes_t']
        boxes_i = []
        ## For each label, update the annotation with the index start and stop times
        ## If you want to do something fancier here, you could change y0,y1 to be specific frequency bands
        y0,y1 = (0,len(f))
        for l in range(len(wav_annot['Labels'])):
            label = labels[l]
            t_start,t_stop = boxes_t[l]
            x0,x1 = find_time(ts,t_start,t_stop)
            boxes_i.append([x0,y0,x1,y1])
        wav_annot['Boxes_i'] = boxes_i
    return annot_df

if __name__ == '__main__':
    wav_dir = sys.argv[1]
    spect_dir = sys.argv[2]
    if len(sys.argv) > 3:
        annot_file = sys.argv[3]
        annot_file = os.path.abspath(annot_file)
        annot_df = parse_annotation(annot_file)
    wav_dir = os.path.abspath(wav_dir)
    spect_dir = os.path.abspath(spect_dir)

    annot_df = make_annotation(wav_dir,annot_file)
    annot_df.to_csv('output_annotation.csv')
    print('All done!')
