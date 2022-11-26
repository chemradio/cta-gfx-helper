import time
from typing import Callable
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.responders.main_responder import Responder
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from container_interaction.orders_db import add_order_to_db


async def results_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE, caller: Callable
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    try:
        if update.callback_query.data not in ["results_correct", "results_incorrect"]:
            raise Exception()

        await update.callback_query.answer(cache_time=180)
        await update.callback_query.edit_message_text(
            text=update.callback_query.message.text
        )

        if update.callback_query.data == "results_correct":
            user_data.update(
                {
                    "results_correct": True,
                    "stage": "results_confirmed",
                    "order_creation_end_timestamp": int(time.time()),
                }
            )
            return await caller(update, context)
        else:
            user_data.clear()
            return await Responder.results.results_incorrect(user_id)

    except:
        return await Responder.errors.gp_error(user_id)
