# -*- coding: utf-8 -*-
from gtts import gTTS
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy import signal
from scipy.fftpack import fft
import numpy as np
import sox

# Define FFT params:-------------------------------------------------------
windowSize =212
shiftSize = 160
nFFT = 1024
window_py = signal.hamming(windowSize)
nOverlap_py = windowSize-shiftSize

words = [u"Эй",u"клач",u"плач", u"мурзач"]
wavs = [w+".wav" for w in words]

def save_tts(words):
    for w in words:
        print "Processing word ",w
        tts = gTTS(text=w,lang='ru',slow=True)
        tts.save(w+'.mp3');
        print "got tts result"
        waud = AudioSegment.from_mp3(w+'.mp3')
        waud.export(w+".wav", format="wav")

def fft_beat(name):
    rate, data = wav.read( name+'.wav')
    #data = data[:,1]
    f,t,Sxx = signal.spectrogram(data,fs=rate,window=window_py,
            noverlap=nOverlap_py,nfft=nFFT,detrend='constant',return_onesided=True,
            scaling='spectrum',mode='complex')

    print Sxx
    plt.pcolormesh(t, f, abs(Sxx))
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()
    #jfft_out = fft(data)
    #jplt.plot(data, np.abs(fft_out))
    #jplt.show()

fft_beat(u'мурзач')
# create combiner
cbn = sox.Combiner()
# pitch shift combined audio up 3 semitones
cbn.pitch(3.0)
# convert output to 8000 Hz stereo
cbn.convert(samplerate=8000)
# create the output file
cbn.build(wavs, 'output.wav', 'concatenate')


