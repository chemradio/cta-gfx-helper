from pathlib import Path

from fastapi import BackgroundTasks, FastAPI

from create_volume_folders import create_volume_folders
from screenshots.screenshot_order_processor import process_screenshot_orders

create_volume_folders()

app = FastAPI()


@app.post("/start_screenshoting")
async def start_screenshooting(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_screenshot_orders)
    return True
