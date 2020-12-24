import os
import logging
from re import A
from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path

from telegram import (
    InlineQueryResultArticle,
    ParseMode,
    InputTextMessageContent,
    Update
)
from telegram.ext import (
    Updater,
    InlineQueryHandler,
    CommandHandler,
    CallbackContext
)
from telegram.utils.helpers import escape_markdown

import stockM

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)
TOKEN = os.getenv("TOKEN")


# Define a few command handlers. These usually take the two arguments update
# and context. Error handlers also receive the raised TelegramError object
# in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        "Hi! Welcome to Stock Updates Slave. "
        "To start using, use the `/` commands to explore the list of build "
        "in commands.",
    )


def get_px_change(update: Update, context: CallbackContext) -> None:
    stocks = update.message.text.split("/get_px_change")[1].strip()
    stocks = stocks.split()
    for _, stock in enumerate(stocks):
        pct_chng = stockM.Ticker(stock).get_price_change()
        update.message.reply_text(
            f"{stock} changed by {pct_chng}%"
        )


def main() -> None:
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("get_px_change", get_px_change))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()