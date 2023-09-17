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

IS_DOCKER = os.getenv("IS_DOCKER")


class Readspeed(Enum):
    SLOW = 140
    MEDIUM = 160
    FAST = 180


REQUEST_TYPE_TEMP_MAP = {
    "video_auto": Responses.request_options.video_auto,
    "video_files": Responses.request_options.video_files,
    "video_mixed": Responses.request_options.video_mixed,
    "only_screenshots": Responses.request_options.only_screenshots,
    "readtime": Responses.request_options.readtime,
}


# containers
DISPATCHER_NAME = (
    os.getenv("dispatcher_name", "dispatcher") if IS_DOCKER else "localhost"
)
DISPATCHER_NODE_PORT = os.getenv("dispatcher_port", 9000)
DISPATCHER_NODE_URL = f"http://{DISPATCHER_NAME}:{DISPATCHER_NODE_PORT}"


# orders
DISPATCHER_ORDERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/admin/db_manipulation/orders"
ADD_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/universal/orders"

# process quote string api
DISPATCHER_STRING_PROCESSOR_ENDPOINT = f"{DISPATCHER_NODE_URL}/helpers/text_processor"


# users
DISPATCHER_USERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/universal/users"
ADD_USER_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}"
EDIT_USER_ENDPOINT = f"{DISPATCHER_NODE_URL}/admin/db_manipulation/users/telegram"

LIST_USERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/admin/db_manipulation/users"

ALLOWED_USERS_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}/allowed"
BLOCKED_USERS_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}/blocked"
PENDING_USERS_ENDPOINT = f"{DISPATCHER_USERS_ENDPOINT}/pending"

BACKUP_DB_ENDPONT = f"{DISPATCHER_NODE_URL}/database/backup"
RESTORE_DB_ENDPONT = f"{DISPATCHER_NODE_URL}/database/restore"

DB_BACKUP_FILE_PATH = "./db_backup.json"
DB_BACKUP_FILE_TEMP_PATH = "./db_backup_temp"

STORAGE_UNIT_NAME = os.getenv("storage_unit_name", "storage_unit")
STORAGE_UNIT_PORT = os.getenv("storage_unit_port", 9010)
STORAGE_UNIT_URL = f"http://{STORAGE_UNIT_NAME}:{STORAGE_UNIT_PORT}/file"

MAX_ATTACHMENT_SIZE = 100000000000
