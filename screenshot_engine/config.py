import os
from pathlib import Path

IS_DOCKER = os.environ.get("IS_DOCKER")
logged_in_to_social_websites = True

SCREENSHOT_FOLDER = Path().cwd() / "volume" / "screenshots"

DPI_MULTIPLIER = 2.0


LOGIN_REQUIRED = ("facebook", "twitter", "instagram")


DISPATCHER_NODE_HOSTNAME = (
    os.getenv("dispatcher_name", "dispatcher")
    if os.environ.get("IS_DOCKER")
    else "localhost"
)
DISPATCHER_NODE_PORT = os.getenv("dispatcher_port", 9000)
# containers
DISPATCHER_NAME = os.getenv("dispatcher_name", "dispatcher")
DISPATCHER_NODE_URL = f"http://{DISPATCHER_NAME}:{DISPATCHER_NODE_PORT}"


DISPATCHER_NODE_URL = f"http://{DISPATCHER_NODE_HOSTNAME}:{DISPATCHER_NODE_PORT}"

LIST_ORDERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders/list"
GET_ONE_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/intercontainer/orders"

EDIT_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/intercontainer/orders"


TWO_LAYER_LINKS = ("facebook", "twitter", "instagram", "telegram")

SOCIAL_WEBSITES = {
    "facebook": "https://facebook.com",
    "twitter": "https://twitter.com",
    "instagram": "https://instagram.com",
}

VOLUME_MOUNTPOINT = Path.cwd() / "volume"

COOKIE_FILE = VOLUME_MOUNTPOINT / "cookie_file" / "cookie_file.json"


# !!!
SELENIUM_HOSTNAME = (
    os.getenv("screenshot_selenium_name", "screenshot_selenium")
    if IS_DOCKER
    else "localhost"
)
REMOTE_SCREENSHOT_DRIVER_URL = f"http://{SELENIUM_HOSTNAME}:4444/wd/hub"


USE_REMOTE_DRIVER = True
SCREENSHOT_ATTEMPTS = 2

AD_DB_URL = "https://raw.githubusercontent.com/chemradio/cta-chrome-extension/main/ads_database.json"


SCREENSHOT_ASPECT_RATIO = [1, 3]
RESOLUTION_MULTIPLIER = 1920
SCREENSHOT_DIMENSIONS = [
    aspect * RESOLUTION_MULTIPLIER for aspect in SCREENSHOT_ASPECT_RATIO
]
