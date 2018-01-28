# -*- coding: utf-8 -*-
from gtts import gTTS
from pydub import AudioSegment
import codecs
import numpy as np
import json
import os
import sox
import time
import sys
from settings import *
import os.path
reload(sys)
if "DISPLAY" not in os.environ:
		import matplotlib
		matplotlib.use('Agg')
sys.setdefaultencoding('utf-8')
UPD = True


def load_words(filename):
    lyr = codecs.open(filename,encoding='utf-8')
    words=lyr.read().decode('utf-8')
    print words
    words=words.replace(",", "").replace('\n',' ').split(' ')
    words=[w for w in words if len(w)>0]
    lyr.close()
    print (words)
    ww=[]
    i=0
    print len(words)
    while i<len(words):
        if len(words[i])<3:
            ww.append(' '.join(words[i:i+3]))
            i = i+3
        elif len(words[i])<5:
            ww.append(' '.join(words[i:i+2]))
            i = i+2
        else:
            ww.append(' '.join(words[i:i+1]))
            i+=1
    print ww
    print len(ww)
    words=ww
    #words=' '.join(words)
    f = open('lyrics.json','w+')
    f.write(json.dumps(words, ensure_ascii=False).encode('utf-8'))
    f.close()
    words= json.load(open('lyrics.json'))

    words = json.loads(json.dumps(words))
    #print [w.encode('utf-8') for w in words]
    words=[w for w in words if len(w)>0]
    return words

def save_tts(words):    
    for w in set(words):
        if len(w)==0:
            continue
        if  os.path.isfile(TMP_DIR+w.replace(' ','%20')+'.mp3') :
            print "skipping"+w.replace(' ','%20')
            continue
        print "Processing word ",w
        tts = gTTS(text=w,lang='ru',slow=False)
        w = w.replace(' ','%20')
        tts.save(TMP_DIR+w+'.mp3')
        print "got tts result"

def add_adlib(user_id, loudness = -6.0):
	files = os.listdir(ADLIB_DIR+str(user_id))
	print files
	fil = sorted(files)[0]
	print "found %i files for user %i"%(len(files),user_id)
	loop_sample = AudioSegment.empty()
	beat = AudioSegment.from_wav("result.wav")
	loop_sample+= AudioSegment.from_wav(ADLIB_DIR+str(user_id)+'/'+fil)
	num_loops = beat.duration_seconds/(loop_sample.duration_seconds+1)
	print "looping user files %i times"%num_loops
    
	loop_quiet = loop_sample*int(num_loops )+ loudness
	result = beat.overlay(loop_quiet)
	result.export("result.wav", format="wav")

def effects(words,voice_speed = 1.2):
    for w in set(words):
        w = w.replace(' ','%20')
        waud = AudioSegment.from_mp3(TMP_DIR+w+'.mp3')
        waud.export(ORIG_DIR+'orig'+w+".wav", format="wav")
        cbn = sox.Transformer()
        cbn.pitch(-5)
        cbn.treble(11.0)
        #cbn.allpass(50)
        #cbn.bass(5.)
        #cbn.flanger(delay=10)
        cbn.reverb(reverberance=20)
        cbn.gain(gain_db=1.0)
        #cbn.noiseprof('orig'+w+'.wav','noiseprof')
        #cbn.noisered('noizeprof', amount=0.5)
        cbn.tempo(voice_speed)
        cbn.loudness(1.0)
        #cbn.convert(samplerate=8000)
        # create the output file
        cbn.build(ORIG_DIR+'orig'+w+'.wav', WAV_DIR+w+'.wav')

if __name__ == "__main__":
    # execute only if run as a script
    if (UPD):
        save_tts(words)
    effects(words)
