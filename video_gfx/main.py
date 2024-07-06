import uuid

import pydantic
from fastapi import UploadFile

import config
from shared import QueueManager, app, purge_storage
from src import main_videogfx

purge_storage(config.STORAGE_PATH)


queue = QueueManager(
    storage_path=config.STORAGE_PATH,
    dispatcher_url=config.DISPATCHER_NOIFICATION_URL,
    operator=main_videogfx,
    remote_driver_url_list=config.SELENIUM_CONTAINERS_LOCAL,
)


class VideoGFXOrderIn(pydantic.BaseModel):
    background_file: UploadFile
    foreground_file: UploadFile | None = None
    audio_file: UploadFile | None = None
    quote_enabled: bool | None = False
    quote_text: str | None = None
    quote_author_enabled: bool | None = None
    quote_author_text: str | None = None
    template: str | None = None

    secret_key: str | None = None


@app.post("/")
async def capture_screenshots(
    videogfx_order: VideoGFXOrderIn,
) -> str:
    order_id = str(uuid.uuid4())
    queue.append(
        {
            "order_id": order_id,
            "background_file": videogfx_order.background_file,
            "foreground_file": videogfx_order.foreground_file,
            "audio_file": videogfx_order.audio_file,
            "quote_enabled": videogfx_order.quote_enabled,
            "quote_text": videogfx_order.quote_text,
            "quote_author_enabled": videogfx_order.quote_author_enabled,
            "quote_author_text": videogfx_order.quote_author_text,
            "template": videogfx_order.template,
        }
    )
    queue.start_processing()
    return order_id
