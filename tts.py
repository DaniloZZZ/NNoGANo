
# -*- coding: utf-8 -*-
from gtts import gTTS
from pydub import AudioSegment
import codecs
import numpy as np
import json
import sox

words= json.load(open('words.json'))
lyr = codecs.open('lyrics.txt',encoding='utf-8')
words=lyr.read().replace(",", "").split(' ')
#print np.array(words).astype('U')
print (words)
#print [w.encode('utf-8') for w in words]
lyr.close()

wavs = [w+".wav" for w in words]

def save_tts(words):    
    for w in set(words):
        print "Processing word ",w
        tts = gTTS(text=w,lang='ru',slow=False)
        tts.save(w+'.mp3');
        print "got tts result"
        waud = AudioSegment.from_mp3(w+'.mp3')
        waud.export('orig'+w+".wav", format="wav")
        cbn = sox.Transformer()
        # pitch shift combined audio up 3 semitones
        cbn.pitch(-3.0)
        cbn.convert(samplerate=8000)
        # create the output file
        cbn.build('orig'+w+'.wav', w+'.wav')

save_tts(words)
