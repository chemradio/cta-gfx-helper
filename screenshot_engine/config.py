import os
from pathlib import Path

DPI_MULTIPLIER = 2.0
SCREENSHOT_DIMENSIONS = [1920, 5760]
SCREENSHOT_ATTEMPTS = 2

AD_DB_URL = "https://raw.githubusercontent.com/chemradio/cta-chrome-extension/main/ads_database.json"

SCREENSHOT_FOLDER = Path().cwd() / "storage"
COOKIE_FILE = Path().cwd() / "storage" / "cookie_file.json"

LOGIN_REQUIRED = ("facebook", "twitter", "instagram")
TWO_LAYER_LINKS = ("facebook", "twitter", "instagram", "telegram")
SOCIAL_WEBSITES = {
    "facebook": "https://facebook.com",
    "twitter": "https://twitter.com",
    "instagram": "https://instagram.com",
}

IS_DOCKER = os.environ.get("IS_DOCKER", False)

DISPATCHER_NODE_URL = f"http://dispatcher:9000"
REMOTE_SCREENSHOT_DRIVER_URL = f"http://screenshot_selenium:4444/wd/hub" if IS_DOCKER else "http://localhost:4444/wd/hub"
USE_REMOTE_DRIVER = True



