import os
from enum import Enum
from pathlib import Path

from telegram.constants import ParseMode

from telegram_bot.responders.bot_texts import Responses

BOT_ADMIN = int(os.environ.get("BOT_ADMIN"))
GLOBAL_MESSAGE_PARSE_MODE = ParseMode.HTML
VOLUME_MOUNTPOINT = Path().cwd() / "volume"
USER_FILES_FOLDER = VOLUME_MOUNTPOINT / "user_files"
COOKIE_FILE_PATH = VOLUME_MOUNTPOINT / "cookie_file" / "cookie_file.json"

FILE_DOWNLOAD_TIMEOUT = 180
MAX_AUDIO_LENGTH = 40


class Readspeed(Enum):
    SLOW = 140
    MEDIUM = 160
    FAST = 180


REQUEST_TYPE_TEMP_MAP = {
    "video_auto": Responses.request_options.video_auto,
    "video_files": Responses.request_options.video_files,
    "only_screenshots": Responses.request_options.only_screenshots,
    "readtime": Responses.request_options.readtime,
}


# containers
DISPATCHER_NODE_HOSTNAME = "dispatcher" if os.environ.get("IS_DOCKER") else "localhost"
DISPATCHER_NODE_PORT = 9000
DISPATCHER_NODE_URL = f"http://{DISPATCHER_NODE_HOSTNAME}:{DISPATCHER_NODE_PORT}"


# orders
DISPATCHER_ORDERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders"
ADD_ORDER_ENDPOINT = f"{DISPATCHER_ORDERS_ENDPOINT}/add"


# users
DISPATCHER_USERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/users"
ADD_USER_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}/add"
EDIT_USER_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}/edit"


ALLOWED_USERS_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}/allowed"
BLOCKED_USERS_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}/blocked"
PENDING_USERS_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}/pending"

BACKUP_DB_ENDPONT = f"{DISPATCHER_NODE_URL}/database/backup"
RESTORE_DB_ENDPONT = f"{DISPATCHER_NODE_URL}/database/restore"

DB_BACKUP_FILE_PATH = "./db_backup.json"
DB_BACKUP_FILE_TEMP_PATH = "./db_backup_temp"
