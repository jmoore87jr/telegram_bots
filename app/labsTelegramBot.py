import logging
import requests
import time 
from datetime import datetime
import tweepy 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import create_api 
import credentials

# TODO: separate file; have the bot respond to requests for info on specific player
#   /status <Player>
#   /today <Player>
#   /box <home> <away>
# TODO: dockerize the application
# TODO: run on AWS EC2 micro

class MyStreamListener(tweepy.StreamListener):

    # API endpoint to send message with Telegram bot
    ENDPOINT = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"

    # using top 50 BPM for now
    PLAYERS_TO_TRACK = ['Nikola Jokic', 'Giannis Antetokounmpo', 'Joel Embiid',
                        'LeBron James', 'Stephen Curry', 'Jimmy Butler',
                        'Luka Doncic', 'Kawhi Leonard', 'James Harden',
                        'Damian Lillard', 'Nikola Vucevic', 'Bam Adebayo',
                        'Zion Williamson', 'Kyrie Irving', 'Joe Ingles',
                        'Karl-Anthony Towns', 'Rudy Gobert', 'Tobias Harris',
                        'Bradley Beal', 'Paul George', 'Chris Paul', 
                        'Julius Randle', 'Shai Gilgeous-Alexander', 'Jrue Holiday',
                        'Thaddeus Young', 'Mike Conley', 'DeMar DeRozan',
                        'Donovan Mitchell', 'Jayson Tatum', 'Chris Boucher',
                        'Zach LaVine', 'Trae Young', 'Montrezl Harrell',
                        'Domantas Sabonis', 'Mikal Bridges', 'Clint Capela',
                        'Kyle Anderson', 'LaMelo Ball', 'Jaylen Brown',
                        'Delon Wright', 'Brandon Ingram', 'Jarrett Allen',
                        'Fred VanVleet', 'Michael Porter Jr.', 'Ben Simmons',
                        'John Collins', 'Kristaps Porzingis', 'Terry Rozier',
                        'Jamal Murray', 'T.J. McConnell']

    def on_status(self, status):

        txt = status.text
        dt = status.created_at.strftime("%H:%M:%S")
        auth = status.author.screen_name

        logging.info(f"{dt} -- {txt}")

        # mirror only the relevant tweets
        if any(plyr in txt for plyr in self.PLAYERS_TO_TRACK) and (auth == "FantasyLabsNBA"):
            msg = f"{dt} -- {txt}"
    
            # send message to telegram on new tweet
            url = self.ENDPOINT.format(credentials.TELEGRAM_BOT_API_KEY,
                                       credentials.TELEGRAM_CHANNEL_ID, 
                                       msg)
            requests.get(url)

            return True

def listen():
    """Start listening to the twitter feed"""
    # create api
    api = create_api()

    # create stream
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # filter stream
    myStream.filter(follow=["3444040513"], languages=['en'])


if __name__ == "__main__":
    listen()
