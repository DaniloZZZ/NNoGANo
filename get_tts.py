# -*- coding: utf-8 -*-
from gtts import gTTS
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy import signal
from scipy.fftpack import fft
import json
import numpy as np
import sox
from optparse import OptionParser

from settings import *

def fft_pow(name,low_pass=False):
    # Define FFT params:-------------------------------------------------------
    print "fft from "+name
    windowSize =512
    shiftSize = 160
    nFFT = 1024
    window_py = signal.hamming(windowSize)
    nOverlap_py = windowSize-shiftSize
    rate, data = wav.read( WAV_DIR+name+'.wav')
    if(len(data.shape)>1):
        data = data[:,1]
    #data = data[len(data)/10:len(data)/6]
    f,t,Sxx = signal.spectrogram(data,fs=rate,window=window_py,
            noverlap=nOverlap_py,nfft=nFFT,detrend='constant',return_onesided=True,
            scaling='spectrum',mode='complex')
    if(low_pass):
        Sxx_sc = [ np.divide(s,(f+2))[:5] for s in Sxx.T]
    else:
        Sxx_sc=Sxx.T
    Pow = [sum(abs(s)) for s in Sxx_sc] 
    #plt.pcolormesh(t, f, abs(Sxx))
    '''
    plt.figure(figsize=(20,10))
    plt.plot(t,Pow)
    plt.savefig('pow.png')
    plt.clf()
    fs = np.fft.fft(Pow)
    freq = np.fft.fftfreq(t.shape[-1])
    plt.figure(figsize=(20,10))
    plt.plot(freq,abs(fs))
    plt.show()
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.savefig('ff.png')
    '''
    return Pow,t

def mark_beats(P,t):
    print "marking beats"
    #hist,brd = np.histogram(P,bins=range(7))
    #plt.hist(P)
    #plt.show()
    thr = max(P)*0.65
    print "Power threshhold:",thr
    plt.figure(figsize=(20,10))
    plt.plot(t,P)
    plt.plot(t,np.ones(len(t))*thr)
    plt.savefig('pow.png')

    times =t[P>thr] 
    return times

def place_words(words,beat_filename,times):
    # throwing out 2 first beats, yus to start later
    #np.set_printoptions(threshold='nan')
    print "Beat accent times:",times
    #times =  times[2:] 
    beat = AudioSegment.from_wav(WAV_DIR+beat_filename+".wav")
    tidx = 0
    idx=0
    result=AudioSegment.empty()
    for w in words:
        w = w.replace(' ','%20')
        try:
            p,t = fft_pow(w)
            emph = t[np.argmax(p)]
            emph=0
            sl = AudioSegment.silent((times[idx]-tidx-emph)*1000)
            waud = AudioSegment.from_wav(WAV_DIR+w+".wav")
        except IOError :
            continue
        print "placing word %s at %f idx:%i. word dur:%f"%(w,times[idx],idx,waud.duration_seconds)
        result+=sl+waud
        tidx = result.duration_seconds
        for i, t in enumerate(times):
            # find next beat 
            if t>tidx:  
                idx=i
                break
    result = beat.overlay(result)
    result.export("result.wav", format="wav")
    return result

if __name__ == "__main__":
    # execute only if run as a script
    (options, args) = parser.parse_args()
    BEATFNAME = args[0]
    parser = OptionParser()
    words= json.load(open('lyrics.json'))
    wavs = [w+".wav" for w in words]
    P,t = fft_pow(BEATFNAME,low_pass=True)
    tms = mark_beats(P,t)
    place_words(words,BEATFNAME,tms)

