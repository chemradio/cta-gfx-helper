from telegram import Update
from telegram.ext import ContextTypes

from telegram_bot.responders.main_responder import Responder


async def back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if not context.user_data:
        context.user_data.clear()
        return await Responder.errors.no_active_session(user_id)
    if context.user_data.get("status") == "init":
        context.user_data.clear()
        return await Responder.errors.no_active_session(user_id)

    # shared
    stage = context.user_data.get("stage")
    # match stage:
    #     case "quote_enabled"
