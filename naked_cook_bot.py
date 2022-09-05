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
URL = "https://api.thecatapi.com/v1/images/search"


def new_cat():
    response = requests.get(URL).json()
    return response[0].get("url")


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Завтрак'], ['Обед'], ['Ужин']])

    if chat.last_name is None:
        context.bot.send_message(
            chat_id=chat.id,
            text="Привет {}".format(chat.first_name),
            reply_markup=button
        )
    else:
        context.bot.send_message(
            chat_id=chat.id,
            text="Привет, {} {}".format(chat.first_name, chat.last_name),
            reply_markup=button
        )


def for_errors(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=f"К сожалению, я не смог распознать твою команду:(\nПопробуй команду ниже;)",
        reply_markup=button
    )


def TextHandler(update, context):
    id = update.effective_chat.id
    chat = update.message.text
    print(update)
    if 'Завтрак' in chat:
        context.bot.send_message(
            chat_id=id,
            text='С добрым утром. \nНовый рецепт специально для тебя :)'
        )
        breakfast(update, context)
    elif 'Обед' in chat:
        context.bot.send_message(
            chat_id=id,
            text='Добрый день. \nПриготовим что-нибудь вкусненькое ;)\nСегодня у нас: '
        )
        lunch(update, context)   
    else:
        for_errors(update, context)


updater.dispatcher.add_handler(CommandHandler("start", wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, TextHandler))
updater.dispatcher.add_handler(MessageHandler(Filters.all, for_errors))

updater.start_polling()
updater.idle()
