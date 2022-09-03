import os

import dotenv
import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater,
                          Filters,
                          MessageFilter,
                          CommandHandler)


dotenv.load_dotenv()

token = os.getenv("TOKEN")
updater = Updater(token=token)
URL = ""

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
