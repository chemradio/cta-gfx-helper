import uuid
from pathlib import Path

import pydantic
from fastapi import UploadFile
from fastapi.staticfiles import StaticFiles

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
    framerate: int | float = config.DEFAULT_FRAMERATE
    audio_offset: float = config.DEFAULT_AUDIO_OFFSET
    videogfx_tail: float = config.DEFAULT_VIDEOGFX_TAIL
    secret_key: str | None = None


# videogfx server
app.mount(
    "/",
    StaticFiles(directory=Path.cwd().resolve()),
    name="static",
)


@app.post("/")
async def create_video_gfx(
    videogfx_order: VideoGFXOrderIn,
) -> str:
    order_id = str(uuid.uuid4())
    queue.append(
        {"order_id": order_id, **videogfx_order.model_dump(exclude=("secret_key",))}
    )
    queue.start_processing()
    return order_id
