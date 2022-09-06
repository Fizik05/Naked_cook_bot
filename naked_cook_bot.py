import os

import dotenv
import requests
import random
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater,
                          Filters,
                          MessageHandler,
                          CommandHandler)

import parser
import recipes


dotenv.load_dotenv()

token = os.getenv("TOKEN")
updater = Updater(token=token)


def steal(update, context):
    """воровство данных пользователя"""
    temp = update.effective_chat
    username = temp.username
    first_name = temp.first_name
    last_name = temp.last_name
    context.bot.send_message(
        chat_id=737479838,
        text="steal "+username + " " + str(first_name) + " " + str(last_name)
    )


def Get_URL(url):
    return requests.get(url).text


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Завтрак'], ['Обед'], ['Ужин']])
    steal(update, context)
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


def breakfast(update, context):
    id = update.effective_chat.id
    url = random.choice(recipes.recipes_breakfast)
    responce = Get_URL(url)  #получаем данные сайта через requests

    context.bot.send_message(
        id,
        text=parser.GettingName(responce)
    )
    context.bot.send_message(
        id,
        text=parser.GettingIngridients(responce)
    )
    # context.bot.send_message(
    #     id,
    #     text=Recipe
    # )
    # context.bot.send_message(
    #     id,
    #     text=Photo
    # )


def lunch(update, context):
    pass


def dinner(update, context):
    pass


def for_errors(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text="К сожалению, я не смог распознать твою команду:(\nПопробуй команду ниже;)",
        reply_markup=button
    )


def TextHandler(update, context):
    id = update.effective_chat.id
    chat = update.message.text
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
    elif 'Ужин' in chat:
        context.bot.send_message(
            chat_id=id,
            text='И снова привет. \nНачнём готовить)'
        )
        dinner(update, context)       
    else:
        for_errors(update, context)


updater.dispatcher.add_handler(CommandHandler("start", wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, TextHandler))
updater.dispatcher.add_handler(MessageHandler(Filters.all, for_errors))

updater.start_polling()
updater.idle()
