import os

import dotenv
import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater,
                          Filters,
<<<<<<< Updated upstream
                          MessageHandler,
=======
                          MessageFilter,
>>>>>>> Stashed changes
                          CommandHandler)


dotenv.load_dotenv()

token = os.getenv("TOKEN")
updater = Updater(token=token)
URL = ""

<<<<<<< Updated upstream

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
=======
def wake_up(update, context):
    chat = update.effective_chat

    context.bot.send_message(
        chat_id=chat.id,
        text="Hi, my name is Naked Cook",
    )


def main():
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
>>>>>>> Stashed changes
