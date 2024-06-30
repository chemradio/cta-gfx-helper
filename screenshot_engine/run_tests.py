from pathlib import Path

from src.admin.cookie_generator import generate_cookies
from src.screenshot_processor import parse_capture_screenshots

COOKIE_FILE_PATH = Path.cwd() / "storage" / "cookie_file.json"
REMOTE_DRIVER_URL = "http://localhost:4444/wd/hub"
TARGET_URL = "https://x.com/GeniusGTX/status/1807056930193723595"


parse_capture_screenshots(TARGET_URL, REMOTE_DRIVER_URL, COOKIE_FILE_PATH, 2)
