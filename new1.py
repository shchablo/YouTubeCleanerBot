#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
#Arthur be here
"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from config import TOKEN
import logging
import re
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ONE, TWO, THREE = range(3)

# Пришлите ссылку на видео YouTube
# Define a few command handlers. These usually take the two arguments update and
# context.
def youtube_link_command(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Оставьте сообщение в формате: время текст. Например 01:01:01 - котику страшно.')
    return ONE

def tip_1_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Пришлите ссылку на видео YouTube')

def time_commit(update: Update, context: CallbackContext) -> None:
    msg = update.message.text
    print(msg)
    result = re.findall(r'\d:[0-5]\d:[0-5]\d', msg)
    print(str(result))
    if len(result) >= 1:
        update.message.reply_text(str(result))
        return TWO

def video_command(update: Update, context: CallbackContext):
    """Send a message when the command /video or take it form db is issued."""
    update.message.reply_text("Look at this https://youtu.be/dQw4w9WgXcQ?t=34! Видео для олдов ")
    return THREE

def Done(update: Update, context: CallbackContext):
    """Send a message when the command /Done or take it form db is issued."""
    update.message.reply_text("DONE")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Начнём! /start \n'
                              'Получить видео на проверку /video \n'
                              'Для чего это всё? /new1 \n'
                              'Уведомить о неполадках /new2 \n'
                              'Статистика /new3 \n' #для админов
                              'Отправить видео на рассмотрение /new4 \n' #для админов
                              'Предложить видео /new5 \n'
                              )
    return TWO


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    # dispatcher.add_handler(CommandHandler("help", help_command))
    # dispatcher.add_handler(CommandHandler("video", video_command))
    dispatcher.add_handler(CommandHandler("tip_1", tip_1_command))

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?'), youtube_link_command), ],
        states={
            ONE: [MessageHandler(Filters.text & ~Filters.command, time_commit), ],
            TWO: [CommandHandler("help", video_command), ],
            THREE: [MessageHandler(Filters.regex('^[-\w.]+@([A-z0-9][-A-z0-9]+\.)+[A-z]{2,4}$'), help_command), ]
        },
            fallbacks=[MessageHandler(Filters.regex('да'), Done)],
    )

    # on non command i.e message - echo the message on Telegram
    #dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(conv_handler)
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()