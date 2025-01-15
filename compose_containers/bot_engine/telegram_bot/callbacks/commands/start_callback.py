import time
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.responders.main_responder import Responder


async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    context.user_data.clear()
    context.user_data.update(
        {"status": "init", "order_start_timestamp": int(time.time())}
    )
    return await Responder.start.ask_order_type(user_id)
