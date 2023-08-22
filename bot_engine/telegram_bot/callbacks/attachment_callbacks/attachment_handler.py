from typing import Callable

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

    stored_file_filename = await store_file_in_storage_unit(
        filename=telegram_file.file_id,
        file_bytes=await telegram_file.download_as_bytearray(),
        mime_type=mime_type,
    )

    return stored_file_filename


async def store_file_in_storage_unit(
    filename: str, file_bytes: bytes, mime_type: str
) -> str:
    """Send a HTTP Post request to the central dispatcher node
    for further processing. On success dispatcher node returns
    filename with which the file was stored in storage unit."""
    response = requests.post(
        f"{config.DISPATCHER_NODE_URL}/user_files/",
        files={"upload_file": (filename, file_bytes, mime_type)},
    )
    response.raise_for_status()
    return response.json()["filename"]
