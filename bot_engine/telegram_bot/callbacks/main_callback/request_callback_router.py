from telegram import Update
from telegram.ext import ContextTypes

import config
from telegram_bot.callbacks.commands.start_callback import start_callback
from telegram_bot.callbacks.only_screenshots.only_screenshots_callback import (
    only_screenshots_callback,
)
from telegram_bot.callbacks.readtime.readtime_callback import readtime_callback
from telegram_bot.callbacks.video_auto.video_auto_callback import video_auto_callback
from telegram_bot.callbacks.video_files.video_files_callback import video_files_callback
from telegram_bot.responders.bot_texts import Responses


async def request_type_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
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
            text=f"{Responses.command.start_message_edited} {config.REQUEST_TYPE_TEMP_MAP[update.callback_query.data]}"
        )
    except:
        raise WrongRequestTypeResponse()


async def request_router(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Routing request", flush=True)
    user_data = context.user_data
    user_request_type = user_data.get("request_type")
    print(f"{user_request_type=}", flush=True)

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
            raise WrongRequestTypeResponse
        # else:
        #     return await start_callback(update, context)


class WrongRequestTypeResponse(Exception):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return f"Request type response is wrong. Callback query result is missing or invalid."
