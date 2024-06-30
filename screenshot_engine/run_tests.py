from pathlib import Path

from src.admin.cookie_generator import generate_cookies

COOKIE_FILE_PATH = Path.cwd() / "storage" / "cookie_file.json"
REMOTE_DRIVER_URL = "http://localhost:4444/wd/hub"

TARGET_URL = "https://meduza.io"

generate_cookies(REMOTE_DRIVER_URL, COOKIE_FILE_PATH)
