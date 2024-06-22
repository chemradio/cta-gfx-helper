import os
from pathlib import Path

SCREENSHOT_FOLDER = Path().cwd() / "storage"
COOKIE_FILE = Path().cwd() / "storage" / "cookie_file.json"

IS_DOCKER = os.environ.get("IS_DOCKER", False)

DISPATCHER_NODE_URL = f"http://dispatcher:9000"

REMOTE_SELENIUM_URL = f"http://screenshot_selenium:4444/wd/hub"
