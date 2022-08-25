import telebot
import os
import requests


DATA_API_URL = os.environ.get("APP_DATA_API_URL")

API_TOKEN = os.environ.get('APP_TELEGRAM_TOKEN')

bot = telebot.TeleBot(API_TOKEN)


# TODO Process /help intro message

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi there, I am Sweight.")

    user_id = message.from_user.id
    resp = requests.post(f"{DATA_API_URL}/users/register", json={"id": user_id})

    if resp.status_code == requests.codes.ok:
        bot.reply_to(message, "Пользователь зарегистрирован")

    elif resp.status_code == requests.codes.conflict:
        bot.reply_to(message, "Пользователь уже существует")

        data = resp.json()

        if data.get("user").get("is_active") == False:
            resp = requests.patch(f"{DATA_API_URL}/users/{user_id}/activate")

    else:
        bot.reply_to(message, "Что-то пошло не так. Попробуйте позже.")


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.reply_to(message, "Stopping")

    user_id = message.from_user.id
    resp = requests.patch(f"{DATA_API_URL}/users/{user_id}/deactivate")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
