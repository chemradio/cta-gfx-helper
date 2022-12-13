from pathlib import Path

logged_in_to_social_websites = False

SCREENSHOT_FOLDER = Path().cwd() / "volume" / "screenshots"

DPI_MULTIPLIER = 2.0


LOGIN_REQUIRED = ("facebook", "twitter", "instagram")


DISPATCHER_NODE_HOSTNAME = "dispatcher"
DISPATCHER_NODE_PORT = 9000


DISPATCHER_NODE_URL = f"http://{DISPATCHER_NODE_HOSTNAME}:{DISPATCHER_NODE_PORT}"

LIST_ORDERS_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders/list"
GET_ONE_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders/get_one"

# !!!
EDIT_ORDER_ENDPOINT = f"{DISPATCHER_NODE_URL}/orders/edit"
# EDIT_ORDER_ENDPOINT = f"http://localhost:{DISPATCHER_NODE_PORT}/orders/edit"


TWO_LAYER_LINKS = ("facebook", "twitter", "instagram", "telegram")

SOCIAL_WEBSITES = {
    "facebook": "https://facebook.com",
    "twitter": "https://twitter.com",
    "instagram": "https://instagram.com",
}

VOLUME_MOUNTPOINT = Path.cwd() / "volume"

COOKIE_FILE = VOLUME_MOUNTPOINT / "cookie_file.json"


# !!!
REMOTE_SCREENSHOT_DRIVER_URL = f"http://screenshot_selenium:4444/wd/hub"
# REMOTE_SCREENSHOT_DRIVER_URL = f"http://localhost:4444/wd/hub"


USE_REMOTE_DRIVER = True
SCREENSHOT_ATTEMPTS = 2

AD_DB_URL = "https://raw.githubusercontent.com/chemradio/cta-chrome-extension/main/ads_database.json"