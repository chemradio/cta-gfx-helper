import os
from pathlib import Path

DISPATCHER_NOIFICATION_URL = f"http://dispatcher:9000"
IS_DOCKER = os.environ.get("IS_DOCKER", False)

DPI_MULTIPLIER = 2
SCREENSHOT_FOLDER = Path().cwd() / "storage"
COOKIE_FILE = Path().cwd() / "cookie_file" / "cookie_file.json"
SCREENSHOT_ATTEMPTS = 2

# AD_DB_URL = "https://raw.githubusercontent.com/chemradio/cta-chrome-extension/main/ads_database.json"
REMOTE_DRIVER_URL = (
    f"http://screenshot_selenium:4444/wd/hub"
    if IS_DOCKER
    else "http://localhost:4444/wd/hub"
)
