import time
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.responders.main_responder import Responder


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id

    # unnecessary check
    # if context.user_data:
    #     if len(context.user_data) > 1 or context.user_data.get("status") != "init":
    #         return await Responder.common.terminate_sessions_notification(user_id)

    context.user_data.clear()
    context.user_data.update(
        {"status": "init", "order_start_timestamp": int(time.time())}
    )
    return await Responder.start.ask_order_type(user_id)
