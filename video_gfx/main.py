import uuid
from pathlib import Path

import pydantic

import config
from shared import QueueManager, app, purge_storage

purge_storage(config.STORAGE_PATH)


queue = QueueManager(
    storage_path=config.STORAGE_PATH,
    dispatcher_url=config.DISPATCHER_NOIFICATION_URL,
    operator=main_capture,
    # remote_driver_url=config.REMOTE_DRIVER_URL,
    # cookie_file_path=config.COOKIE_FILE,
    # dpi_multiplier=config.DPI_MULTIPLIER,
    # attempts=config.SCREENSHOT_ATTEMPTS,
)


class VideoGFXOrderIn(pydantic.BaseModel):

    screenshot_link: str
    secret_key: str | None = None


@app.post("/")
async def capture_screenshots(
    videogfx_order: VideoGFXOrderIn,
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
