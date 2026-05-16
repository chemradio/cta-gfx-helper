import os
from pathlib import Path

DISPATCHER_NOIFICATION_URL = f"http://dispatcher:9000"
IS_DOCKER = os.environ.get("IS_DOCKER", False)

DPI_MULTIPLIER = 2
SCREENSHOT_FOLDER = Path().cwd() / "storage"
COOKIE_FILE = Path().cwd() / "cookie_file" / "cookie_file.json"
SCREENSHOT_ATTEMPTS = 2

# Screenshot-capture backend switch.
#   "selenium"   - legacy: remote Selenium node, CDP capture via the driver.
#   "playwright" - in-container headless Chromium, same CDP capture, no
#                  remote Selenium node needed.
# Both paths keep the proven CDP device-emulation + Page.captureScreenshot
# workflow; only the browser transport changes. The stored cookie file is
# always in Selenium format - the playwright backend converts it to/from
# Playwright's cookie schema automatically, so no manual flag is needed.
SCREENSHOT_BACKEND = "playwright"
# SCREENSHOT_BACKEND = "selenium"

REMOTE_DRIVER_URL = (
    f"http://screenshot_selenium:4444/wd/hub"
    if IS_DOCKER
    else "http://localhost:4444/wd/hub"
)
