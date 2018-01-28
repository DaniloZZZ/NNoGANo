
from pydub import AudioSegment
from optparse import OptionParser

def mp3towav(filepath,fr,to):
    waud = AudioSegment.from_mp3(filepath+'.mp3')
    waud=waud[1000*fr:to*1000]
    waud.export(filepath+".wav", format="wav")

def wavtomp3(filepath,fr,to):
    print "convertiong to mp3"
    waud = AudioSegment.from_wav(filepath+'.wav')
    waud=waud[1000*fr:to*1000]
    waud.export(filepath+".mp3", format="mp3")

if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option("-f", "--from", dest="fr",type="float",
                          help="trim from", metavar="FILE")
    parser.add_option("-t", "--to",
                          dest="to",type="float", default=True,
                                            help="don't print status messages to stdout")
    (options, args) = parser.parse_args()
    print args
    w = args[0]
    mp3towav(w,options.fr,options.to)
