from fastapi import FastAPI, UploadFile

import config
from screenshots.screenshot_capture.attempt_screenshot_capture import (
    attempt_screenshot_capture,
)
    attempt_screenshot_capture
# shared imports / shared between screenshooter and video_gfx containers
from shared.fastapi_routers import file_server, order_check
from shared.models.probably_trash.screenshot_order import ScreenshotOrderIn
from shared.queue_manager.queue_manager import QueueManager

app = FastAPI()
app.include_router(file_server.router, prefix="/file_server")
app.include_router(order_check.router)
queue = QueueManager(attempt_screenshot_capture)


@app.post("/")
async def capture_screenshots(
    screenshot_order: ScreenshotOrderIn,
) -> str:
    order_id = queue.append({"screenshot_link": screenshot_order.screenshot_link})
    queue.start_processing()
    return order_id


@app.post("/cookie_file")
async def create_cookie_file(upload_file: UploadFile):
    print("Request for storing cookie file.")
    with open(config.COOKIE_FILE, "wb") as f:
        f.write(upload_file.file.read())
    return "Cookie file stored."
