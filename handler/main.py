import telebot
import os
import requests

from lib.i18n import Internationalization as I18n


DATA_API_URL = os.environ.get("APP_DATA_API_URL")

API_TOKEN = os.environ.get("APP_TELEGRAM_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

app_language = os.environ.get("APP_LANG", "en")
i18n = I18n(lang=app_language)


# TODO Process /help intro message


@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    resp = requests.post(f"{DATA_API_URL}/users/register", json={"id": user_id})

    if resp.status_code == requests.codes.ok:
        bot.reply_to(message, "{registration_ok}".format(**i18n.lang_map))

    elif resp.status_code == requests.codes.conflict:
        bot.reply_to(message, "{registration_err_conflict}".format(**i18n.lang_map))

        data = resp.json()

        if data.get("user").get("is_active") is False:
            resp = requests.patch(f"{DATA_API_URL}/users/{user_id}/activate")

    else:
        bot.reply_to(message, "{registration_err_unknown}".format(**i18n.lang_map))


@bot.message_handler(commands=["welcome"])
def welcome(message):
    bot.reply_to(message, "{welcome}".format(**i18n.lang_map))


@bot.message_handler(commands=["stop"])
def stop(message):
    bot.reply_to(message, "Stopping")

    user_id = message.from_user.id
    requests.patch(f"{DATA_API_URL}/users/{user_id}/deactivate")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
