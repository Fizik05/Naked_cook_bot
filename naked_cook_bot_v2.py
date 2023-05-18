import os
import random

import dotenv
import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
)


dotenv.load_dotenv()

token = os.getenv("TOKEN")
updater = Updater(token=token)


class Users:
    def __init__(self, recipe_url: str, number_of_step: int, cnt_steps: int):
        self.recipe_url = recipe_url
        self.number_of_step = number_of_step
        self.cnt_steps = cnt_steps


users = {}


def steal(update, context):
    chat = update.effective_chat
    name = chat.first_name
    last_name = chat.last_name
    context.bot.send_message(
        chat_id="932006021",
        text=f"{name} {last_name}"
    )


def wake_up(update, context):
    chat = update.effective_chat
    users[str(chat.id)] = Users("", 1, 0)
    button = ReplyKeyboardMarkup(
                                 [['Завтрак', 'Обед', 'Ужин'],],
                                 resize_keyboard=True
                                )
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


def get_response(url):
    response = requests.get(url).json()
    return response


def get_id(recipes):
    recipes_id = []

    for recipe in recipes:
        recipes_id.append(recipe["id"])

    return recipes_id


def cooking_by_steps(update, context):
    user_id = update.effective_chat.id

    button = ReplyKeyboardMarkup(
        [
            ["Следующий шаг"],
            ["Закончить готовку"]
        ],
        resize_keyboard=True
    )
    instruction = get_response(
        f"{users[str(user_id)].recipe_url}"
        "instructions/"
        f"{users[str(user_id)].number_of_step}"
        "/"
    )
    instruction = instruction["text"]
    context.bot.send_message(
        chat_id=user_id,
        text=instruction,
        reply_markup=button
    )

    users[str(user_id)].number_of_step += 1
    if users[str(user_id)].number_of_step > users[str(user_id)].cnt_steps:
        users[str(user_id)] = Users("", 1, 0)
        context.bot.send_message(
            chat_id=user_id,
            text="На этом мы закончили, надеюсь вам понравилось;)",
            reply_markup=ReplyKeyboardMarkup(
                [['/start']],
                resize_keyboard=True
            )
        )


def start_cooking(update, context, category):
    user_id = update.effective_chat.id
    category_url = f"http://127.0.0.1:8000/api/v2/recipes/{category}/"

    recipes = get_response(category_url)
    ids = get_id(recipes)
    recipe_url = f"http://127.0.0.1:8000/api/v2/recipes/{random.choice(ids)}/"
    users[str(user_id)].recipe_url = recipe_url
    current_recipe = get_response(recipe_url)

    context.bot.send_message(
        chat_id=user_id,
        text=current_recipe['title']
    )

    button = ReplyKeyboardMarkup(
        [
            ["Начать готовку"],
            ["Главное меню"]
        ],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=user_id,
        text=f"Ингредиенты:\n{current_recipe['ingredients']}",
        reply_markup=button
    )

    instructions_url = recipe_url + "instructions/"
    instructions = get_response(instructions_url)
    users[str(user_id)].cnt_steps = len(instructions)


def TextHandler(update, context):
    id = update.effective_chat.id
    text = update.message.text

    if "Завтрак" in text:
        context.bot.send_message(
            chat_id=id,
            text="С добрым утром😴\nНовый рецепт специально для тебя :)",
        )
        start_cooking(update, context, "lunch")

    elif "Обед" in text:
        context.bot.send_message(
            chat_id=id,
            text='Добрый день.\nПриготовим что-нибудь вкусненькое ☺️\n' +
                 'Сегодня у нас: '
        )
        start_cooking(update, context, "lunch")

    elif "Ужин" in text:
        context.bot.send_message(
            chat_id=id,
            text='И снова привет.\nНачнём готовить🙃'
        )
        start_cooking(update, context, "dinner")

    elif "Закончить готовку" in text:
        button = ReplyKeyboardMarkup([["/start"]], resize_keyboard=True)
        context.bot.send_message(
            chat_id=id,
            text="Надеюсь тебе понравилось❤️\n" +
                 "Чтобы попробовать ещё раз введи команду  '/start'",
            reply_markup=button
        )

    elif "Начать готовку" in text or "Следующий шаг" in text:
        cooking_by_steps(update, context)

    elif "Главное меню" in text:
        button = ReplyKeyboardMarkup(
            [['Завтрак', 'Обед', 'Ужин']],
            resize_keyboard=True
        )
        context.bot.send_message(
            chat_id=id,
            text="Ну, давай попробуем ещё разок",
            reply_markup=button
        )
        users[str(id)] = Users("", 1, 0)

    else:
        button = ReplyKeyboardMarkup([['/start']], resize_keyboard=True)

        context.bot.send_message(
            chat_id=id,
            text="К сожалению, я не смог распознать твою команду:(\n" +
                 "Попробуй команду ниже😉",
            reply_markup=button
        )


updater.dispatcher.add_handler(CommandHandler("start", wake_up))
updater.dispatcher.add_handler(MessageHandler(Filters.text, TextHandler))

updater.start_polling()
updater.idle()
