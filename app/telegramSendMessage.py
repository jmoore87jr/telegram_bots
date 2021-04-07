import logging
import requests
import time 
import json
import pprint
from datetime import datetime
from config import create_api 
import tweepy 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

ENDPOINT = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
TELEGRAM_BOT_API_KEY = "1752570785:AAE3bp5-8r1ozzmDf4c_XPaXwkMz1qM18SY"
TELEGRAM_CHANNEL_ID = "-1001294167477"

def getUpdates():
    """Get info about our Telegram bot including Channel ID"""
    
    r = requests.post("https://api.telegram.org/bot1752570785:AAE3bp5-8r1ozzmDf4c_XPaXwkMz1qM18SY/getUpdates")
    print(r.status_code)
    r_dict = r.json()

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(r_dict)

def sendMessage():
    req = ENDPOINT.format(TELEGRAM_BOT_API_KEY,
                          TELEGRAM_CHANNEL_ID, 
                          "Hello")
    requests.get(req)

    return True

if __name__ == "__main__":
    sendMessage()