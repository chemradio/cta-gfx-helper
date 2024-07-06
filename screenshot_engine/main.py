import uuid

import pydantic
from fastapi import UploadFile

import config
from shared import QueueManager, app, purge_storage
from src import main_capture
from src.helpers.driver_auth import initialize_cookie_storage

purge_storage(config.SCREENSHOT_FOLDER)
initialize_cookie_storage(config.COOKIE_FILE)

queue = QueueManager(
    storage_path=config.SCREENSHOT_FOLDER,
    dispatcher_url=config.DISPATCHER_NOIFICATION_URL,
    operator=main_capture,
    remote_driver_url=config.REMOTE_DRIVER_URL,
    cookie_file_path=config.COOKIE_FILE,
    dpi_multiplier=config.DPI_MULTIPLIER,
    attempts=config.SCREENSHOT_ATTEMPTS,
)


class ScreenshotOrderIn(pydantic.BaseModel):
    screenshot_link: str
    secret_key: str | None = None


@app.post("/")
async def capture_screenshots(
    screenshot_order: ScreenshotOrderIn,
) -> str:
    order_id = str(uuid.uuid4())
    queue.append(
        {
            "order_id": order_id,
            "screenshot_link": screenshot_order.screenshot_link,
        }
    )
    queue.start_processing()
    return order_id


@app.post("/cookie_file")
async def create_cookie_file(upload_file: UploadFile):
    print("Request for storing cookie file.")
    with open(config.COOKIE_FILE, "wb") as f:
        f.write(upload_file.file.read())
    return "Cookie file stored."
