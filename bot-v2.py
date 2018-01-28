# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputFile
from io import BytesIO
import logging
import pickle
import os
from urllib2 import urlopen, URLError, HTTPError
import random
import Generate_Rap
from tts import *
from get_tts import *
from audio_helper import *

import settings

#TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
TELEGRAM_TOKEN = '521957216:AAFBuP4he_DGOzo9AovExQfExDQ3jJ8W1vA'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Bot:
    def __init__(self):
        self.last_command = None
        self.waiting = False
        self.uploaded_audio = 0
        self.beat_file_name = 'beat'+str(random.randrange(1,8))

        self.logger = logging.getLogger(__name__)

        self.updater = Updater(TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher

        help_handler = CommandHandler('help', self.help)
        easypeasy_handler = CommandHandler('easypeasy', self.easypeasy)
        setbro_handler = CommandHandler('setbro', self.setbro)
        setmood_handler = CommandHandler('setmood', self.setmood)
        record_handler = CommandHandler('record', self.record)

        message_handler = MessageHandler(Filters.text, self.text_handler)
	audio_handler = MessageHandler(Filters.voice, self.voice_handler)

        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(audio_handler)

        self.dispatcher.add_handler(setmood_handler)
        self.dispatcher.add_handler(record_handler)
        self.dispatcher.add_handler(setbro_handler)
        self.dispatcher.add_handler(easypeasy_handler)
        self.dispatcher.add_handler(help_handler)

        self.dispatcher.add_error_handler(self.error)

        self.updater.start_polling()

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def text_handler(self, bot, update):
        chat_id = update.message.chat_id
        text = update.message.text.lower().split()
        if self.last_command == 'easypeasy':
            message = bot.send_message(text="Cейчас все будет...",
                                     chat_id=chat_id)

            self.work_with_easypeasy(text, chat_id)
            message = bot.send_audio(audio=open('result.mp3'),
                                     chat_id=chat_id)
            print "DONE"
        elif self.last_command == 'setbro':
            pass
        elif self.last_command == 'setmood':
            pass
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=random.choice(settings.NEUTRAL_MESSAGES))
        self.last_command = None

    def voice_handler(self, bot, update):
        chat_id = update.message.chat_id
        print 'get audio'
        if self.last_command == 'record':
            message = bot.send_message(text="Делаем рэп из твоего шедревра...",
                                     chat_id=chat_id)
            self.work_with_record(bot.getFile(update.message.voice.file_id), chat_id)
            message = bot.send_audio(audio=open('result.mp3'),
                                     chat_id=chat_id)
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=random.choice(settings.NEUTRAL_MESSAGES))
        self.last_command = None

    def work_with_easypeasy(self, text, chat_id):
        if len(text) < 5:
            text += settings.EXTRA_WORDS[:5 - len(text)]
        print "Opening lyrics file. words: %s,id%i" % (text, chat_id)
        text = Generate_Rap.main(*text)[:20]
        print text
        save_tts(text)
        effects(text)
        self.beat_file_name = 'beat'+str(random.randrange(8))
        P, t = fft_pow(self.beat_file_name, low_pass=True)
        tms = mark_beats(P, t)
        place_words(text, self.beat_file_name, tms)
        wavtomp3('result',0,45)
        print "Created Track."

    def work_with_record(self, voice_path, chat_id):
        try:
            link = urlopen(voice_path.file_path)
            print 'downloading voice'
            if not os.path.exists(settings.ADLIB_DIR + str(chat_id)):
                os.makedirs(settings.ADLIB_DIR + str(chat_id))
            local_file=open((settings.ADLIB_DIR + str(chat_id) + '/' + str(self.uploaded_audio) + '.ogg'), 'w+') 
            data = link.read()
            self.uploaded_audio+=1
            local_file.write(data)
            local_file.close()
            text = Generate_Rap.main(*settings.EXTRA_WORDS)[:10]
            #text = ['отладка',"фууу"]
            print text
            save_tts(text)
            effects(text)
            self.beat_file_name = 'beat'+str(random.randrange(8))
            P, t = fft_pow(self.beat_file_name, low_pass=True)
            tms = mark_beats(P, t)
            place_words(text, self.beat_file_name, tms)
            print "Created Track."
            add_adlib(chat_id)
            print "ADLIB Track."
            wavtomp3('result',0,45)
            print "converted Track."
        except Exception as e:
            print "Can not download user's voice message"
            print e
        #

    def record(self, bot, update):
        self.last_command = 'record'
        bot.send_message(chat_id=update.message.chat_id,
                         text=settings.RECORD_MESSAGE)

    def setmood(self, bot, update):
        self.last_command = 'setmood'
        bot.send_message(chat_id=update.message.chat_id,
                         text=settings.SETMOOD_MESSAGE)

    def setbro(self, bot, update):
        self.last_command = 'setbro'
        bot.send_message(chat_id=update.message.chat_id,
                         text=settings.SETBRO_MESSAGE)

    def easypeasy(self, bot, update):
        self.last_command = 'easypeasy'
        bot.send_message(chat_id=update.message.chat_id,
                         text=settings.EASYPEASY_MESSAGE)

    @staticmethod
    def help(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text=settings.HELP_MESSAGE)


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    bio = BytesIO()
    bot = Bot()
