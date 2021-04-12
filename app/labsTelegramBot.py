import logging
import requests
import time 
from datetime import datetime
import tweepy 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import create_api 
import credentials
import players

# TODO: separate file; have the bot respond to requests for info on specific player
#   /status <Player>
#   /today <Player>
#   /box <home> <away>
# TODO: run on AWS EC2 micro

def msg_telegram(msg, auth):
    # API endpoint to send message with Telegram bot
    endpoint = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"

    # mirror only the relevant tweets
    if any(plyr in msg for plyr in players.PLAYERS_TO_TRACK) and (auth == "FantasyLabsNBA"):

        # send message to telegram on new tweet
        url = endpoint.format(credentials.TELEGRAM_BOT_API_KEY,
                              credentials.TELEGRAM_CHANNEL_ID, 
                              msg)
        requests.get(url)

        return True


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        txt = status.text
        dt = status.created_at.strftime("%H:%M:%S")
        auth = status.author.screen_name

        msg = f"{dt} -- {txt}"

        # log
        logging.info(msg)

        # send message to telegram
        msg_telegram(msg, auth)

    def on_exception(self, exception):
        print(f"EXCEPTION: {exception}")
        return

    def on_error(self, status_code):
        print(f"STATUS CODE: {status_code}")
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False
        return

        # returning non-False reconnects the stream, with backoff.


def listen():
    """Start listening to the twitter feed"""
    # create api
    api = create_api()

    while True:
        try:
            # create stream
            myStreamListener = MyStreamListener()
            myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

            # filter stream
            myStream.filter(follow=["3444040513"], languages=['en'])
        except:
            continue



if __name__ == "__main__":
    listen()
