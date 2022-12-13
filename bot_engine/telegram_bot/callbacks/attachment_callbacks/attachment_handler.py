import secrets
from typing import Callable

import config
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.callbacks.attachment_callbacks.attachment_exceptions import (
    AudioDurationExceeded,
    WrongAudioFormat,
)
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


async def attachment_downloader(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    caller: Callable = None,
) -> str:
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

    save_file_name = config.USER_FILES_FOLDER / f"user_{secrets.token_hex(8)}"
    try:
        downloaded_file: str = await target_function(bald_message, save_file_name)
    except WrongAudioFormat as e:
        print(e)
        Responder.errors.wrong_audio_format(user_id)
    except AudioDurationExceeded as e:
        print(e)
        Responder.errors.audio_duration_exceeded(user_id)

    return downloaded_file
