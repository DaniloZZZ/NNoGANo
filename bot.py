from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputFile
from io import BytesIO
import logging
import pickle
import os


bio = BytesIO()

TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def echo(bot, update):
    splited_text = update.message.text.lower()
    print "MSG"
    chat_id = update.message.chat.id
    update.message.reply_text("BIENE!")
    message = bot.send_audio(audio=open('result.wav'),
			     chat_id=chat_id)

RESPONSES = {
    "Hello": ["Hi there!", "Hi!", "Welcome!", "Hello, {name}!"],
    "Hi there": ["Hello!", "Hello, {name}!", "Hi!", "Welcome!"],
    "Hi!": ["Hi there!", "Hello, {name}!", "Welcome!", "Hello!"],
    "Welcome": ["Hi there!", "Hi!", "Hello!", "Hello, {name}!",],
}
def human_response(message):
    leven = fuzzywuzzy.process.extract(message.get("text", ""), RESPONSES.keys(), limit=1)[0]
    response = {'chat_id': message['chat']['id']}
    if leven[1] < 75:
        response['text'] = "I can not understand you"
    else:
        response['text'] = random.choice(RESPONSES.get(leven[0])).format_map(
            {'name': message["from"].get("first_name", "")}
        )
    return response

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def help_message(arguments, message):
    response = {'chat_id': message['chat']['id']}
    result = ["Hey, %s!" % message["from"].get("first_name"),
              "\rI can accept only these commands:"]
    for command in CMD:
        result.append(command)
    response['text'] = "\n\t".join(result)
    return response

def main():
    updater = Updater(TELEGRAM_TOKEN)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
