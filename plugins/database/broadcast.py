# ©️ amangautamdev | @LegendRobot | AMAN_WORLD

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import logging
import config  # Importing config.py file

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to read bot token from config.py
def read_token_from_config():
    return config.BOT_TOKEN

# List to store chat IDs of subscribers
subscribers = set()

# Command handler to start the bot
def start(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    if chat_id not in subscribers:
        subscribers.add(chat_id)
        update.message.reply_text('Welcome! You will now receive broadcast messages.')
    else:
        update.message.reply_text('Welcome back! You are already subscribed to broadcast messages.')

# Command handler to send broadcast message
def broadcast_message(update: Update, context: CallbackContext) -> None:
    if not subscribers:
        update.message.reply_text('There are no subscribers to broadcast to.')
        return
    message = ' '.join(context.args)
    for subscriber in subscribers:
        context.bot.send_message(subscriber, message)
    update.message.reply_text('Broadcast message sent to all subscribers.')

# Command handler to send broadcast message by admin
def send_broadcast(update: Update, context: CallbackContext) -> None:
    if not subscribers:
        update.message.reply_text('There are no subscribers to send a broadcast message to.')
        return
    if update.message.from_user.id != config.OWNER_ID:
        update.message.reply_text('You are not authorized to send broadcast messages.')
        return
    message = ' '.join(context.args)
    for subscriber in subscribers:
        context.bot.send_message(subscriber, message)
    update.message.reply_text('Broadcast message sent to all subscribers.')

# Function to run the bot
def run_bot():
    # Get the bot token from config
    BOT_TOKEN = read_token_from_config()

    # Create the Updater and pass it the bot's token
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("broadcast", broadcast_message))
    dispatcher.add_handler(CommandHandler("send_broadcast", send_broadcast))  # Add send_broadcast command

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

