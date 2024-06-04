from ..config import IS_DOCKER

LOGIN_REQUIRED = ("facebook", "twitter", "instagram")
TWO_LAYER_LINKS = ("facebook", "twitter", "instagram", "telegram")
USE_REMOTE_DRIVER = True


DPI_MULTIPLIER = 2.0
SCREENSHOT_DIMENSIONS = [1920, 5760]
SCREENSHOT_ATTEMPTS = 2

AD_DB_URL = "https://raw.githubusercontent.com/chemradio/cta-chrome-extension/main/ads_database.json"
REMOTE_SCREENSHOT_DRIVER_URL = (
    f"http://screenshot_selenium:4444/wd/hub"
    if IS_DOCKER
    else "http://localhost:4444/wd/hub"
)
