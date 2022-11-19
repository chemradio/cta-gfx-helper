from telegram import Update
from telegram.ext import CallbackContext
from pprint import pprint


def all_handler(update: Update, context:CallbackContext):
    # get auth

    # get init

    # get request type
        # send to appropriate callback

    

    pprint(update.to_dict())
    return update.message.reply_text('catch')