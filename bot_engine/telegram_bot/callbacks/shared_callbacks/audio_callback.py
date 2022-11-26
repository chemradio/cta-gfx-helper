from typing import Callable
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.callbacks.attachment_callbacks.attachment_handler import (
    attachment_downloader,
)
from telegram_bot.responders.main_responder import Responder
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id


async def audio_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE, caller: Callable
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    try:
        if stage == "audio_enabled":
            if update.callback_query.data not in ["audio_enabled", "audio_disabled"]:
                raise Exception()

            await update.callback_query.answer(cache_time=180)
            await update.callback_query.message.delete()
            # await update.callback_query.edit_message_text(
            #     text=update.callback_query.message.text
            # )

            if update.callback_query.data == "audio_enabled":
                user_data.update({"audio_enabled": True, "stage": "audio_file"})
                return await Responder.audio.ask_send_audio(user_id)
            else:
                user_data.update({"audio_enabled": False, "stage": "audio_passed"})
                return await caller(update, context)

        if stage == "audio_file":
            downloaded_file = await attachment_downloader(update, context)
            user_data.update({"audio_path": downloaded_file, "stage": "audio_passed"})
            return await caller(update, context)

    except:
        return await Responder.errors.gp_error(user_id)
