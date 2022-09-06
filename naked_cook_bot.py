from logging.config import dictConfig
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
dictionary = {}


# def steal(update, context):
#     """воровство данных пользователя"""
#     temp = update.effective_chat
#     username = temp.username
#     first_name = temp.first_name
#     last_name = temp.last_name
#     context.bot.send_message(
#         chat_id=737479838,
#         text="steal "+username + " " + str(first_name) + " " + str(last_name)
#     )


def Get_URL(url):
    return requests.get(url).text


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['Завтрак'], ['Обед'], ['Ужин']])
    # steal(update, context)
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


def start_cooking(upd, context):
    id = upd.effective_chat.id
    arr = dictionary[id]
    if arr == []:
        button = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
        context.bot.send_message(
            id,
            text="На этом готовка закончена. Нажмите '/start' чтобы посмотреть ещё один рецепт.",
            reply_markup=button
        )
    else:
        text = arr[0][0]
        image = "https:" + arr[0][1]
        del dictionary[id][0]

        context.bot.send_message(
            id,
            text=text
        )
        context.bot.send_photo(
            id,
            image
        )


def breakfast(update, context):
    try:
        id = update.effective_chat.id
        url = random.choice(recipes.recipes_breakfast)
        response = Get_URL(url)
        button = ReplyKeyboardMarkup([["Следующий шаг"],
                                      ["Закончить готовку"]],
                                     resize_keyboard=True)
        instruction = parser.GettingSteps(response)
        array = []

        for i in instruction:
            array.append([i.description, i.image])

        context.bot.send_message(
            id,
            text=parser.GettingName(response)
        )
        context.bot.send_message(
            id,
            text=parser.GettingIngridients(response),
            reply_markup=button
        )
        dictionary[id] = array
        del array
        start_cooking(update, context)
    except Exception as exs:
        print(exs)
        button = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
        context.bot.send_message(
            id,
            text="У нас произошла ошибка на сервере, пожалуйста попробуйте снова)",
            reply_markup=button
        )


def lunch(update, context):
    try:
        id = update.effective_chat.id
        url = random.choice(recipes.recipes_lunch)
        response = Get_URL(url)
        button = ReplyKeyboardMarkup([["Следующий шаг"],
                                      ["Закончить готовку"]],
                                     resize_keyboard=True)
        instruction = parser.GettingSteps(response)
        array = []

        for i in instruction:
            array.append([i.description, i.image])

        context.bot.send_message(
            id,
            text=parser.GettingIngridients(response),
            reply_markup=button
        )
        dictionary[id] = array
        del array
        start_cooking(update, context)
    except Exception as exs:
        print(exs)
        button = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
        context.bot.send_message(
            id,
            text="У нас произошла ошибка на сервере, пожалуйста попробуйте снова)",
            reply_markup=button
        )


def dinner(update, context):
    try:
        id = update.effective_chat.id
        url = random.choice(recipes.recipes_dinner)
        response = Get_URL(url)
        button = ReplyKeyboardMarkup([["Следующий шаг"],
                                      ["Закончить готовку"]],
                                     resize_keyboard=True)
        instruction = parser.GettingSteps(response)
        array = []

        for i in instruction:
            array.append([i.description, i.image])

        context.bot.send_message(
            id,
            text=parser.GettingName(response)
        )
        context.bot.send_message(
            id,
            text=parser.GettingIngridients(response),
            reply_markup=button
        )
        dictionary[id] = array
        del array
        start_cooking(update, context)
    except Exception as exs:
        print(exs)
        button = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
        context.bot.send_message(
            id,
            text="У нас произошла ошибка на сервере, пожалуйста попробуйте снова)",
            reply_markup=button
        )


def for_errors(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text="К сожалению, я не смог распознать твою команду:(\nПопробуй команду ниже😉",
        reply_markup=button
    )


def TextHandler(update, context):
    id = update.effective_chat.id
    chat = update.message.text
    if 'Завтрак' in chat:
        context.bot.send_message(
            chat_id=id,
            text='С добрым утром😴\nНовый рецепт специально для тебя :)'
        )
        breakfast(update, context)
    elif 'Обед' in chat:
        context.bot.send_message(
            chat_id=id,
            text='Добрый день.\nПриготовим что-нибудь вкусненькое ☺️\nСегодня у нас: '
        )
        lunch(update, context)
    elif 'Ужин' in chat:
        context.bot.send_message(
            chat_id=id,
            text='И снова привет.\nНачнём готовить🙃'
        )
        dinner(update, context)
    elif 'Следующий шаг' in chat:
        start_cooking(update, context)
    elif "Закончить готовку" in chat:
        button = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
        context.bot.send_message(
            chat_id=id,
            text="Надеюсь тебе понравилось❤️\nЧтобы попробовать ещё раз введи команду  '/start'",
            reply_markup=button
        )
        del dictionary[id]
    else:
        for_errors(update, context)


updater.dispatcher.add_handler(CommandHandler("start", wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, TextHandler))
updater.dispatcher.add_handler(MessageHandler(Filters.all, for_errors))

updater.start_polling()
updater.idle()
