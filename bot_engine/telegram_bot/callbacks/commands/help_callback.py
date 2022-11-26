from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.responders.main_responder import Responder


async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    return Responder.help.help(user_id)
