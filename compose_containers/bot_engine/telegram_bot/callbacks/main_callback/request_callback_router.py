from telegram import Update
from telegram.ext import ContextTypes

import config
from ..order_request_callbacks import (
    only_screenshots_callback,
    readtime_callback,
    video_auto_callback,
    video_files_callback,
)
from telegram_bot.responders.main_responder import Responder
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id


async def request_type_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    try:
        user_data.update(
            {
                "request_type": update.callback_query.data,
                "status": "order_creation",
                "stage": "start_order",
            }
        )
        await update.callback_query.answer(cache_time=180)
        await update.callback_query.edit_message_text(
            text=f"🍱 Тип заказа: {config.REQUEST_TYPE_TEMP_MAP[update.callback_query.data]}"
        )
    except:
        print(
            f"Request type response is wrong. Callback query result is missing or invalid."
        )
        return await Responder.errors.gp_error(user_id)


async def request_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = parse_user_id(update)
    user_request_type = context.user_data.get("request_type")

    # route to appropriate callbacks
    match user_request_type:
        case "video_auto":
            return await video_auto_callback(update, context)
        case "video_files":
            return await video_files_callback(update, context)
        case "video_mixed":
            return await video_files_callback(update, context)
        case "only_screenshots":
            return await only_screenshots_callback(update, context)
        case "readtime":
            return await readtime_callback(update, context)
        case _:
            await Responder.errors.custom_error(
                user_id=user_id, error_text="🆘 Неверная команда. Попробуй /start"
            )
            print(
                f"Request type response is wrong. Callback query result is missing or invalid."
            )
            return
