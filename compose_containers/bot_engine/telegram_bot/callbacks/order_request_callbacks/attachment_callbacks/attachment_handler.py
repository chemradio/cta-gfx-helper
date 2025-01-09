from typing import Callable
from io import BytesIO
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.exceptions.attachments import AttachmentNotNeeded, AttachmentTypeMismatch, AttachmentSizeExceeded, AttachmentNotFound
import config
from .attachment_helpers import attachment_finder, reply_to_message_parser
from .file_handlers import audio_handler,photo_handler,document_handler
from py_gfxhelper_lib.files.asset_file import AssetFile
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder

async def attachment_downloader(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    caller: Callable = None,
) -> AssetFile:
    bald_message = await reply_to_message_parser(update)
    available_attachments = await attachment_finder(bald_message)

    if not available_attachments:
        raise AttachmentNotFound()

    user_id = parse_user_id(update)
    stage = context.user_data.get("stage")

    stage_attachment_map = {
        "audio_file": {"audio"},
        "bg_file": {"photo", "document"},
        "fg_file": {"photo", "document"},
        "background_file": {"photo", "document"},
        "main_file": {"photo", "document"},
    }

    # check if we need attachments at this stage
    if stage not in stage_attachment_map:
        # reply with "i dont need attachemnts right now..."
        raise AttachmentNotNeeded()
    
    # check if there are correct attachments for this stage
    for test_stage, allowed_attachemnts in stage_attachment_map.items():
        if stage == test_stage:
            # check if none of the elements of the list "available_attachments" is in the "allowed_attachemnts"
            if not any([attachment in allowed_attachemnts for attachment in available_attachments]):
                # reply with "wrong attachment type..."
                raise AttachmentTypeMismatch()
            break

    # get the actual attachment
    if stage == "audio_file":
        tg_file, mime_type = await audio_handler(bald_message)
    else:
        if "document" in available_attachments:
            tg_file, mime_type = await document_handler(bald_message)
        else:
            tg_file, mime_type = await photo_handler(bald_message)

    # check file size
    if tg_file.file_size > config.MAX_ATTACHMENT_SIZE:
        await Responder.errors.max_attachment_size_exceeded(user_id)
        raise AttachmentSizeExceeded(f"Attachment size exceeded. {tg_file.file_size} is bigger than max size {config.MAX_ATTACHMENT_SIZE}")


    downloaded_file = BytesIO()
    await tg_file.download_to_memory(downloaded_file)

    return AssetFile(bytes_or_bytesio=downloaded_file, mime_type=mime_type)
