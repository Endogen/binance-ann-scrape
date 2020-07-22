#!/usr/bin/python3

import time
import datetime
import requests
import threading

from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

BASE_URL = "https://www.binance.com"

check = True
cache = list()
updtr = Updater("891197415:AAEyQNI2zxf0cBkGg2t0IUVDGcWDcI7JTFk")


def stop(bot, update):
    def _shutdown():
        global check
        check = False

        updtr.stop()
        updtr.is_idle = False

    update.message.reply_text("Stopping...")
    threading.Thread(target=_shutdown).start()


updtr.dispatcher.add_handler(CommandHandler(stop.__name__, stop))
updtr.bot.send_message(134166731, "Starting...")
updtr.start_polling(clean=True)

init = True
while check:
    time.sleep(2)

    response = requests.get(f"{BASE_URL}/en/support/announcement")

    if response.status_code != 200:
        print("Status code " + str(response.status_code))
        continue

    soup = BeautifulSoup(response.content, "html.parser")

    for news in soup.find_all(class_="css-sbrje5"):
        text = news.get_text()

        if init:
            cache.append(text)
            continue

        if text in cache:
            continue
        else:
            print(datetime.datetime.now(), "NEW ENTRY", text)
            url = BASE_URL + news["href"]

            try:
                updtr.bot.send_message(134166731, f"{text}\n\n{url}")
                updtr.bot.send_message(1055475333, f"{text}\n\n{url}")
            except Exception as e:
                print(f"ERROR: {e}")

        cache.append(text)

    init = False
    print(datetime.datetime.now(), "Up to date")
