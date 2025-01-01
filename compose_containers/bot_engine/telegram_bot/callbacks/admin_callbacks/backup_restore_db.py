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


async def backup_db_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = parse_user_id(update)
    is_admin = await ensure_admin(user_id)
    if not is_admin:
        return None

    result = await backup_db_request()
    if not result:
        return None

    with open(DB_BACKUP_FILE_PATH, "w+") as f:
        json.dump(result, f)

    with ZipFile(f"{DB_BACKUP_FILE_PATH}.zip", "w") as zip:
        zip.write(DB_BACKUP_FILE_PATH)

    with open(f"{DB_BACKUP_FILE_PATH}.zip", "rb") as binarified_file:
        await bot.send_document(
            chat_id=user_id,
            document=binarified_file,
            allow_sending_without_reply=True,
            reply_markup=ReplyKeyboardRemove(),
            read_timeout=300,
            write_timeout=300,
            pool_timeout=300,
            connect_timeout=300,
        )

    return await asyncio.sleep(2)


async def restore_db_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    user_id = parse_user_id(update)
    is_admin = await ensure_admin(user_id)
    if not is_admin:
        return None

    # get the attachment
    bald_message = await reply_to_message_parser(update)
    available_attachments = await attachment_finder(bald_message)
    if not available_attachments:
        return False

    file = await bald_message.document.get_file()
    downloaded_file = await file.download_to_drive(
        # custom_path=save_file_name,
        read_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        write_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        connect_timeout=config.FILE_DOWNLOAD_TIMEOUT,
        pool_timeout=config.FILE_DOWNLOAD_TIMEOUT,
    )
    download_path = Path(downloaded_file)
    db_backup_dict = extract_backup(download_path)
    download_path.unlink()

    restore_result = await restore_db_request(db_backup_dict)
    return await bot.send_message(user_id, restore_result)


def extract_backup(backup_path: Path) -> Optional[dict]:
    if backup_path.suffix == ".zip":
        json_path = extract_first_json_from_zip(backup_path)
        if not json_path:
            return False
        with open(json_path, "r") as jf:
            result = json.load(jf)
        if ("users" not in result) or ("orders" not in result):
            return False
        return result


def extract_first_json_from_zip(zip_path: Path) -> Optional[Path]:
    with ZipFile(zip_path, "r") as zip:
        json_files = [
            filename for filename in zip.namelist() if Path(filename).suffix == ".json"
        ]
        if not json_files:
            return False
        json_file = json_files[0]
        return zip.extract(json_file)
