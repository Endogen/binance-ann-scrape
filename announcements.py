#!/usr/bin/python3

import time
import datetime
import requests


from bs4 import BeautifulSoup
from telegram.ext import Updater

BASE_URL = "https://www.binance.com"

news_str = str()

updater = Updater("891197415:AAEyQNI2zxf0cBkGg2t0IUVDGcWDcI7JTFk")

while True:
    time.sleep(2)

    response = requests.get(f"{BASE_URL}/en/support/announcement")

    if response.status_code != 200:
        print("Status code " + str(response.status_code))
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    news = soup.find_all(class_="css-sbrje5")[0]
    text = news.get_text()

    print(f"[{datetime.datetime.now()}]", text, BASE_URL + news["href"])

    if not news_str:
        news_str = text
        continue

    if news_str == text:
        continue

    url = BASE_URL + news["href"]

    try:
        updater.bot.send_message(134166731, f"{text}\n\n{url}")
        updater.bot.send_message(1055475333, f"{text}\n\n{url}")
    except:
        pass
