from typing import Callable
from io import BytesIO
import requests
from telegram import File, Update
from telegram.ext import ContextTypes

import config
from telegram_bot.callbacks.attachment_callbacks.attachment_helpers import (
    attachment_finder,
    reply_to_message_parser,
)
from telegram_bot.callbacks.attachment_callbacks.audio_handler import audio_handler
from telegram_bot.callbacks.attachment_callbacks.document_handler import (
    document_handler,
)
from telegram_bot.callbacks.attachment_callbacks.photo_handler import photo_handler
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder
from custom_types import AssetFile


async def attachment_downloader(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    caller: Callable = None,
) -> AssetFile:
    bald_message = await reply_to_message_parser(update)
    available_attachments = await attachment_finder(bald_message)

    if not available_attachments:
        return None

    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    target_attachments_map = {
        "audio_file": {"audio"},
        "bg_file": {"photo", "document"},
        "fg_file": {"photo", "document"},
        "background_file": {"photo", "document"},
        "main_file": {"photo", "document"},
    }

    target_attachment_types: set = target_attachments_map[stage]
    target_attachment_set = target_attachment_types.intersection(available_attachments)
    if not target_attachment_set:
        return None

    functions_map = {
        "audio": audio_handler,
        "photo": photo_handler,
        "document": document_handler,
    }
    target_function_key = target_attachment_set.intersection(
        set(functions_map.keys())
    ).pop()
    target_function = functions_map[target_function_key]

    telegram_file: File
    mime_type: str
    telegram_file, mime_type = await target_function(bald_message)
    print(f"Telegram File Size: {telegram_file.file_size=}")

    if telegram_file.file_size > config.MAX_ATTACHMENT_SIZE:
        await Responder.errors.max_attachment_size_exceeded(user_id)
        raise Exception()

    downloaded_file = BytesIO()
    await telegram_file.download_to_memory(downloaded_file)
    return AssetFile(
        bytes=downloaded_file,
        mime_type=mime_type,
    )
