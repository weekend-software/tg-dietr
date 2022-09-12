import schedule
import time
import os

DEV_MODE = os.environ.get("APP_DEV_MODE")


def job():
    print("I'm working...")

if not DEV_MODE:
    schedule.every().saturday.at("12:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    job()
