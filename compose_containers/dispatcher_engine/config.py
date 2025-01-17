import os
from pathlib import Path

IS_DOCKER = os.environ.get("IS_DOCKER", False)

STORAGE_PATH = Path.cwd() / "storage"

# telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ADMIN = os.getenv("BOT_ADMIN")
TELEGRAM_SEND_DOCUMENT_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
TELEGRAM_SEND_MESSAGE_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
