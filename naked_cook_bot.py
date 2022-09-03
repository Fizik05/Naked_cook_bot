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
URL = ""


def wake_up(update, context):
    chat = update.effective_chat
    if chat.last_name is None:
        context.bot.send_message(
            chat_id=chat.id,
            text="Привет {}".format(chat.first_name)
        )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text="Привет {} {}".format(chat.first_name, chat.last_name)
        )


def for_errors(update, context):
    pass

    updater.start_polling()
    updater.idle()


updater.dispatcher.add_handler(CommandHandler("start", wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, for_errors))
updater.start_polling()
updater.idle()
