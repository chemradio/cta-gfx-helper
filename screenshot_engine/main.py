from fastapi import FastAPI

from create_volume_folders import create_volume_folders
from screenshots.logic.controllers.auth_controller.cookie_manager import CookieManager
from screenshots.screenshot_order_processor import screenshooter_thread

create_volume_folders()

CookieManager.initialize_cookie_storage()

app = FastAPI()


@app.post("/start_screenshoting")
async def start_screenshooting():
    screenshooter_thread()
    return True
