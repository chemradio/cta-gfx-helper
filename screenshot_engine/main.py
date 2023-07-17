from create_volume_folders import create_volume_folders
from fastapi import FastAPI
from screenshots.screenshot_order_processor import screenshooter_thread

# create_volume_folders()

app = FastAPI()


@app.post("/start_screenshoting")
async def start_screenshooting():
    screenshooter_thread()
    return True
