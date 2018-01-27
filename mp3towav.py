
from pydub import AudioSegment
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-f", "--from", dest="fr",type="float",
                          help="trim from", metavar="FILE")
parser.add_option("-t", "--to",
                          dest="to",type="float", default=True,
                                            help="don't print status messages to stdout")


(options, args) = parser.parse_args()
print args
w = args[0]
waud = AudioSegment.from_mp3(w+'.mp3')
print "trimming from %f to %f"%(options.fr,options.to)
waud=waud[1000*options.fr:options.to*1000]
waud.export(w+".wav", format="wav")
