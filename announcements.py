#!/usr/bin/python3

import sys
import time
import logging
import datetime
import requests
import threading

from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler

BASE_URL = "https://www.binance.com"

last = str()
check = True
cache = list()
updtr = Updater("891197415:AAEyQNI2zxf0cBkGg2t0IUVDGcWDcI7JTFk")

wait = 5
if sys.argv[1:]:
    wait = float(sys.argv[1])


def stop(bot, update):
    def _shutdown():
        global check
        check = False

        updtr.stop()
        updtr.is_idle = False

    update.message.reply_text("Stopping...")
    threading.Thread(target=_shutdown).start()


def state(bot, update):
    update.message.reply_text(f"Happily running...\n\n{last}")


def sleep(bot, update, args):
    try:
        global wait
        wait = float(args[0])
        update.message.reply_text("Done")
    except Exception as ex:
        update.message.reply_text(f"ERROR: {ex}")


updtr.dispatcher.add_handler(CommandHandler(stop.__name__, stop))
updtr.dispatcher.add_handler(CommandHandler(state.__name__, state))
updtr.dispatcher.add_handler(CommandHandler(sleep.__name__, sleep, pass_args=True))

updtr.bot.send_message(134166731, "Starting...")
updtr.start_polling(clean=True)

init = True
while check:
    try:
        time.sleep(wait)

        response = requests.get(f"{BASE_URL}/en/support/announcement", {"timeout": wait})

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
                last = f"[{datetime.datetime.now()}] {text}"
                print(last)

                url = BASE_URL + news["href"]

                updtr.bot.send_message(134166731, f"{text}\n\n{url}")
                updtr.bot.send_message(1055475333, f"{text}\n\n{url}")

            cache.append(text)

        init = False
        print(datetime.datetime.now(), "Up to date")
    except Exception as e:
        msg = f"ERROR: {e}"
        logging.error(msg)
        updtr.bot.send_message(134166731, msg)
