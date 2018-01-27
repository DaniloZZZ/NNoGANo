# -*- coding: utf-8 -*-
from gtts import gTTS
from pydub import AudioSegment
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy.fftpack import fft
import sox

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
    rate, data = wav.read('bells.wav')
    fft_out = fft(data)
    %matplotlib inline
    plt.plot(data, np.abs(fft_out))
    plt.show()

fft_beat('beat')
# create combiner
cbn = sox.Combiner()
# pitch shift combined audio up 3 semitones
cbn.pitch(3.0)
# convert output to 8000 Hz stereo
cbn.convert(samplerate=8000)
# create the output file
cbn.build(wavs, 'output.wav', 'concatenate')


