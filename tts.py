
# -*- coding: utf-8 -*-
from gtts import gTTS
from pydub import AudioSegment
import codecs
import numpy as np
import json
import sox

words= json.load(open('words.json'))
lyr = codecs.open('lyrics.txt',encoding='utf-8')
words=lyr.read().replace(",", "").replace('\n',' ').split(' ')
#print np.array(words).astype('U')
words=[w for w in words if len(w)>0]
lyr.close()
print (words)
f = open('words.json','w+')
f.write(json.dumps(words, ensure_ascii=False).encode('utf-8'))
f.close()
words= json.load(open('lyrics.json'))

words = json.loads(json.dumps(words))
#print [w.encode('utf-8') for w in words]

wavs = [w+".wav" for w in words]

def save_tts(words):    
    for w in set(words):
        if len(w)==0:
            continue
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
