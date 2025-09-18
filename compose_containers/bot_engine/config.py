import os
from enum import Enum
from pathlib import Path

from telegram.constants import ParseMode

BOT_ADMIN = int(os.environ.get("BOT_ADMIN"))


def parse_quote_editors():
    editors_str = os.getenv("QUOTE_EDITORS", "").strip()
    if not editors_str:
        return []

    editors = []
    for editor in editors_str.split(","):
        editor = editor.strip()
        if editor:  # Skip empty strings
            try:
                editors.append(int(editor))
            except ValueError:
                print(
                    f"Warning: Invalid editor ID '{editor}' in QUOTE_EDITORS, skipping"
                )
    return editors


TELEGRAM_QUOTE_EDITORS = parse_quote_editors()
GLOBAL_MESSAGE_PARSE_MODE = ParseMode.HTML
VOLUME_MOUNTPOINT = Path().cwd() / "volume"
USER_FILES_FOLDER = VOLUME_MOUNTPOINT / "user_files"
COOKIE_FILE_PATH = VOLUME_MOUNTPOINT / "cookie_file" / "cookie_file.json"

FILE_DOWNLOAD_TIMEOUT = 180
MAX_AUDIO_LENGTH = 40

IS_DOCKER = os.getenv("IS_DOCKER")


REQUEST_TYPE_TEMP_MAP = {
    "video_auto": "Графика из ссылки",
    "video_files": "Графика из файлов",
    "video_mixed": "Графика из файла + скриншот",
    "only_screenshots": "Только скриншоты",
    "readtime": "Хрон текста",
}


# containers
DISPATCHER_URL = f"http://dispatcher:9000"
# ADMIN_USERS_ENDPOINT = f"{DISPATCHER_URL}/admin/users"
USERS_ENDPOINT = f"{DISPATCHER_URL}/users/"
ORDERS_ENDPOINT = f"{DISPATCHER_URL}/orders/"

# db backup restore
BACKUP_DB_ENDPONT = f"{DISPATCHER_URL}/database/backup"
RESTORE_DB_ENDPONT = f"{DISPATCHER_URL}/database/restore"

DB_BACKUP_FILE_PATH = "./db_backup.json"
DB_BACKUP_FILE_TEMP_PATH = "./db_backup_temp"

MAX_ATTACHMENT_SIZE = 100_000_000_000
