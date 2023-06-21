import os
from pathlib import Path

REGISTER_PASSPHRASE = os.environ.get("REGISTER_PASSPHRASE")

IS_DOCKER = os.environ.get("IS_DOCKER", True)

SQL_SERVER = "temp.sqlite"
SQL_CONNECT_STRING = f"sqlite:///{SQL_SERVER}"
RECENT_ORDERS_INTERVAL_HOURS = 12
VOLUME_MOUNTPOINT = Path.cwd() / "volume"
RENDER_OUTPUT_PATH = VOLUME_MOUNTPOINT / "video_exports"
SCREENSHOTS_FOLDER = VOLUME_MOUNTPOINT / "screenshots"
USER_FILES_FOLDER = VOLUME_MOUNTPOINT / "user_files"
HTML_ASSEMBLIES_FOLDER = VOLUME_MOUNTPOINT / "html_assemblies"

# database configuration
POSTGRES_USER = os.environ.get("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOSTNAME = os.environ.get("POSTGRES_HOSTNAME", "db")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "postgres")
POSTGRES_URL = os.environ.get(
    "POSTGRES_URL",
    f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOSTNAME}:{POSTGRES_PORT}/{POSTGRES_DB}",
)
POSTGRES_URL = f"postgres://postgres:{POSTGRES_PASSWORD}@db:5432/postgres"

SQLITE_URL = "sqlite:///db.sqlite"

DB_CONNECTION_STRING = POSTGRES_URL if IS_DOCKER else "postgres://localhost"


# other containers
SCREENSHOTER_HOSTNAME = os.getenv("screenshoter_name", "screenshoter")
SCREENSHOTER_PORT = int(os.getenv("screenshoter_port", 9002))

VIDEOGFX_HOSTNAME = os.getenv("video_gfx_name", "video_gfx")
VIDEOGFX_PORT = int(os.getenv("video_gfx_port", 9004))

SENDER_HOSTNAME = os.getenv("telegram_sender_name", "sender")
SENDER_PORT = int(os.getenv("telegram_sender_port", 9007))

SCREENSHOTER_ENDPOINT = (
    f"http://{SCREENSHOTER_HOSTNAME}:{SCREENSHOTER_PORT}/start_screenshoting"
)
VIDEOGFX_ENDPOINT = f"http://{VIDEOGFX_HOSTNAME}:{VIDEOGFX_PORT}/start_video_gfx"
SENDER_ENDPOINT = f"http://{SENDER_HOSTNAME}:{SENDER_PORT}/send_orders"

COOKIE_FILE_PATH = VOLUME_MOUNTPOINT / "cookie_file.json"

import secrets

JWT_SECRET = os.environ.get("JWT_SECRET", secrets.token_hex(16))
