import uuid
from pathlib import Path

from fastapi import File, Form, UploadFile
from fastapi.staticfiles import StaticFiles

import config
from shared import QueueManager, app, purge_storage
from shared.utils.asset_file import AssetFile
from src import main_videogfx

purge_storage(config.STORAGE_PATH)


queue = QueueManager(
    storage_path=config.STORAGE_PATH,
    dispatcher_url=config.DISPATCHER_NOIFICATION_URL,
    operator=main_videogfx,
    remote_driver_url_list=config.SELENIUM_CONTAINERS_LOCAL,
)


@app.post("/")
def create_video_gfx(
    background_file: UploadFile = File(...),
    foreground_file: UploadFile | None = File(None),
    audio_file: UploadFile | None = File(None),
    quote_enabled: bool = Form(False),
    quote_text: str | None = Form(None),
    quote_author_enabled: bool = Form(None),
    quote_author_text: str | None = Form(None),
    template: str | None = Form(None),
    framerate: int | float = Form(config.DEFAULT_FRAMERATE),
    audio_offset: float = Form(config.DEFAULT_AUDIO_OFFSET),
    videogfx_tail: float = Form(config.DEFAULT_VIDEOGFX_TAIL),
    animation_duration: float | int = Form(config.DEFAULT_ANIMATION_DURATION),
    secret_key: str | None = Form(None),
) -> str:
    order_id = str(uuid.uuid4())

    queue.append(
        {
            "order_id": order_id,
            "background_file": AssetFile(background_file),
            "foreground_file": AssetFile(foreground_file) if foreground_file else None,
            "audio_file": AssetFile(audio_file) if audio_file else None,
            "quote_enabled": quote_enabled,
            "quote_text": quote_text,
            "quote_author_enabled": quote_author_enabled,
            "quote_author_text": quote_author_text,
            "template": template,
            "framerate": framerate,
            "audio_offset": audio_offset,
            "videogfx_tail": videogfx_tail,
            "animation_duration": animation_duration,
        }
    )
    queue.start_processing()
    return order_id


# videogfx server
app.mount(
    "/",
    StaticFiles(directory=Path.cwd().resolve()),
    name="static",
)
