import schedule
import time
import os
import telebot

DEV_MODE = os.environ.get("APP_DEV_MODE")

API_TOKEN = os.environ.get("APP_TELEGRAM_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

user_id = 187281514

def job():
    bot.send_message(
        user_id,
        "Внесите ваши данные",
    )

if not DEV_MODE:
    schedule.every().saturday.at("12:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    job()
