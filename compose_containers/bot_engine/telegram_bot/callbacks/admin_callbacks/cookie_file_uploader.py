import asyncio
import json
from pathlib import Path
from typing import Optional
from zipfile import ZipFile

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes

import config
from config import DB_BACKUP_FILE_PATH
from container_interaction.backup_restore_db import (
    backup_db_request,
    restore_db_request,
)
from telegram_bot.bot_instance import bot
from telegram_bot.callbacks.admin_callbacks.ensure_admin import ensure_admin
from telegram_bot.callbacks.attachment_callbacks.attachment_helpers import (
    attachment_finder,
    reply_to_message_parser,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder


async def cookie_file_uploader(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    print("entered cookie_file_uploader")
    user_id = parse_user_id(update)
    is_admin = await ensure_admin(user_id)
    if not is_admin:
        return None

    # get the attachment
    bald_message = await reply_to_message_parser(update)
    available_attachments = await attachment_finder(bald_message)
    if not available_attachments:
        print(bald_message)
        print("No available attachments")
        return False

    file = await bald_message.document.get_file()
    downloaded_file = await file.download_to_drive(
        custom_path=config.COOKIE_FILE_PATH,
        read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
    )
    download_path = Path(downloaded_file)

    return await Responder.admin_panel.cookie_file_upload_status(
        config.BOT_ADMIN, download_path.exists()
    )
