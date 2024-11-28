from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.responders.main_responder import Responder


async def exit_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.user_data.get("status"):
        context.user_data.clear()
        return await Responder.exit.exit_missing_order(update.message.from_user.id)
    else:
        context.user_data.clear()
        return await Responder.exit.exit_terminate_order(update.message.from_user.id)
