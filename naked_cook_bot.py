import os

import dotenv
import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater,
                          Filters,
                          MessageHandler,
                          CommandHandler)


dotenv.load_dotenv()

token = os.getenv("TOKEN")
updater = Updater(token=token)
URL = "https://spoonacular.com"


def new_recipe():
    pass


buttons = ReplyKeyboardMarkup([['Завтрак', 'Обед', 'Ужин']])
reply_markup = buttons


def for_errors(update, context):
    updater.start_polling()
    updater.idle()


def wake_up(update, context):
    chat = update.effective_chat
    
    if chat.last_name is None:
        context.bot.send_message(
            chat_id=chat.id,
            text="Привет {}".format(chat.first_name),
        )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text="Привет {} {}".format(chat.first_name, chat.last_name),
        )


def TextHandler(update, context):
    chat = update.effective_chat
    if 'Завтрак' in chat or 'Обед' in chat or 'Ужин' in chat:
        context.bot.send_message(
            chat_id=chat.id,
            text='Рецептов нету, но есть фотки котиков :)'
        )
        newrecipe()
    else:
        for_errors()


updater.dispatcher.add_handler(CommandHandler('start', wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, TextHandler))
updater.start_polling()
updater.idle()

