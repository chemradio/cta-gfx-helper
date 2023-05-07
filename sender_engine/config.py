import os
from pathlib import Path

IS_DOCKER = os.environ.get("IS_DOCKER")

DISPATCHER_NODE_HOSTNAME = os.getenv("dispatcher_name", "dispatcher")
DISPATCHER_NODE_PORT = os.getenv("dispatcher_port", 9000)
DISPATCHER_NODE_URL = f"http://{DISPATCHER_NODE_HOSTNAME}:{DISPATCHER_NODE_PORT}"

LIST_ORDERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders/list"
EDIT_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/intercontainer/orders"
GET_ONE_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/intercontainer/orders"


BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_ADMIN = os.environ.get("BOT_ADMIN")

VOLUME_MOUNTPOINT = Path.cwd() / "volume"
VIDEO_GFX_FOLDER = VOLUME_MOUNTPOINT / "video_exports"
SCREENSHOTS_FOLDER = VOLUME_MOUNTPOINT / "screenshots"

SEND_DOCUMENT_TELEGRAM_API_ENDPOINT = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
)

SEND_MESSAGE_TELEGRAM_API_ENDPOINT = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
)
