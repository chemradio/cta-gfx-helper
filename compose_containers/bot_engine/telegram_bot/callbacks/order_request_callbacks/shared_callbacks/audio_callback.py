from typing import Callable

from telegram import Update
from telegram.ext import ContextTypes
from ..attachment_callbacks.attachment_handler import attachment_downloader
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder
from py_gfxhelper_lib.intercontainer_requests.file_requests import convert_file
from telegram_bot.exceptions.attachments import (
    AttachmentTypeMismatch,
    AttachmentSizeExceeded,
    AttachmentNotFound,
)
from ..attachment_callbacks.attachment_helpers import (
    attachment_finder,
    reply_to_message_parser,
)


async def audio_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE, caller: Callable
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    if stage == "audio_enabled":
        # check if available attachments
        try:
            bald_message = await reply_to_message_parser(update)
            available_attachments = await attachment_finder(bald_message)
            if "audio" in available_attachments:
                user_data.update({"stage": "audio_file"})
                return await audio_callback(update, context, caller)
        except:
            ...

        if update.callback_query.data not in ["audio_enabled", "audio_disabled"]:
            raise Exception("Invalid callback data for audio_callback")

        await update.callback_query.answer(cache_time=180)

        if update.callback_query.data == "audio_enabled":
            user_data.update({"stage": "audio_file"})
            return await Responder.audio.ask_send_audio(user_id)
        else:
            user_data.update({"stage": "audio_passed"})
            return await caller(update, context)

    if stage == "audio_file":
        try:
            downloaded_file = await attachment_downloader(update, context)
            user_data.update(
                {
                    "audio_file": await convert_file(downloaded_file),
                    "stage": "audio_passed",
                }
            )
            return await caller(update, context)
        except AttachmentTypeMismatch:
            return await Responder.errors.custom_error(
                user_id,
                "Не могу обработать аудио. Может не тот файл? Пришли аудио-файл",
            )
        except AttachmentSizeExceeded:
            return await Responder.errors.custom_error(
                user_id, "Размер файла превышает 100 МБ"
            )
        except AttachmentNotFound:
            return await Responder.errors.custom_error(
                user_id, "Не файл... Пришли аудио-файл"
            )
