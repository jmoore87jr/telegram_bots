import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import credentials

# bot token for testBot / FantasyLabsNBA_mirror_bot
token = credentials.TELEGRAM_BOT_API_KEY

# create updater object
updater = Updater(token=token, use_context=True)

# create dispatcher locally for quicker access
dispatcher = updater.dispatcher

# set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# this function is called every time the bot receives a Telegram message that contains the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="Welcome to the @FantasyLabsNBA Twitter mirror bot")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# add echo with MessageHandler
def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                             text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

# takes /caps <text> and replies in all caps
def caps(update, context): # sends message to channel but still requires PM
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=credentials.TELEGRAM_CHANNEL_ID, 
                             text=text_caps)

caps_handler = CommandHandler(command='caps', callback=caps)
dispatcher.add_handler(caps_handler)

"""
# marco polo for chat rather than private message
def marco(update, context):
    context.bot.send_message(chat_id=credentials.TELEGRAM_CHANNEL_ID, 
                             text="polo")

marco_handler = 
"""

# as soon as handlers are added to dispatcher, they are in effect
# start bot
updater.start_polling()
updater.idle()