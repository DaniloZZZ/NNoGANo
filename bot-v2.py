# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputFile
from io import BytesIO
import logging
import pickle
import os
import random
from tts import *
from get_tts import *
import settings

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

class Bot:
    def __init__(self):
        self.last_command = None
        self.waiting = False
        self.beat_file_name = 'bfree'

        self.logger = logging.getLogger(__name__)

        self.updater = Updater(TELEGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher

        help_handler = CommandHandler('help', self.help)
        easypeasy_handler = CommandHandler('easypeasy', self.easypeasy)
        setbro_handler = CommandHandler('setbro', self.setbro)
        setmood_handler = CommandHandler('setmood', self.setmood)
        record_handler = CommandHandler('record', self.record)

        message_handler = MessageHandler(Filters.text, self.text_handler)

        self.dispatcher.add_handler(message_handler)

        self.dispatcher.add_handler(setmood_handler)
        self.dispatcher.add_handler(record_handler)
        self.dispatcher.add_handler(setbro_handler)
        self.dispatcher.add_handler(easypeasy_handler)
        self.dispatcher.add_handler(help_handler)

    def text_handler(self, bot, update):
        chat_id = update.message.chat_id
        text = update.message.text.lower().split()
        if self.last_command == 'easypeasy':
            if len(text) < 5:
                text += settings.EXTRA_WORDS[:5 - len(text)]
            print "Opening lyrics file. words: %s,id%i" % (text, chat_id)
            text *= 5
            save_tts(text)
            effects(text)
            words = json.load(open('lyrics.json'))
            wavs = [w + ".wav" for w in words]
            self.beat_file_name = 'bfree'
            P, t = fft_pow(self.beat_file_name, low_pass=True)
            tms = mark_beats(P, t)
            place_words(text, self.beat_file_name, tms)
            print "Created Track."
            message = bot.send_audio(audio=open('result.wav'),
                                     chat_id=chat_id)
            print "DONE"
        elif self.last_command == 'record':
            pass
        elif self.last_command == 'setbro':
            pass
        elif self.last_command == 'setmood':
            pass
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=random.choice(settings.NEUTRAL_MESSAGES))
        self.last_command = None

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
