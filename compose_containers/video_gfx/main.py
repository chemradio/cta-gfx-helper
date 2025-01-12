import uuid
from pathlib import Path
from pprint import pprint
from fastapi import File, Form, UploadFile
from fastapi.staticfiles import StaticFiles

import config
from py_gfxhelper_lib import QueueManager
from py_gfxhelper_lib.files import AssetFile
from fastapi import FastAPI
from py_gfxhelper_lib.fastapi_routers import order_check_router, file_server_router
from py_gfxhelper_lib.startup import purge_storage
from py_gfxhelper_lib import DBHandler
from src import main_videogfx

DBHandler.init()

purge_storage(config.STORAGE_PATH)

app = FastAPI()
app.include_router(file_server_router)
app.include_router(order_check_router)

from py_gfxhelper_lib.fastapi_routers.order_check import get_db_handler

app.dependency_overrides[get_db_handler] = lambda: DBHandler

queue = QueueManager(
    storage_path=config.STORAGE_PATH,
    dispatcher_url=config.DISPATCHER_NOIFICATION_URL,
    operator=main_videogfx,
    remote_driver_url_list=config.SELENIUM_CONTAINERS,
    assembly_server_url=config.ASSEMBLY_SERVER_URL,
    db_handler=DBHandler,
)


@app.post("/", response_model=dict)
async def create_video_gfx(
    background_file: UploadFile = File(...),
    foreground_file: UploadFile | None = File(None),
    audio_file: UploadFile | None = File(None),
    quote_text: str | None = Form(None),
    quote_author_text: str | None = Form(None),
    template: str | None = Form(None),
    framerate: int | float = Form(config.DEFAULT_FRAMERATE),
    audio_offset: float = Form(config.DEFAULT_AUDIO_OFFSET),
    videogfx_tail: float = Form(config.DEFAULT_VIDEOGFX_TAIL),
    animation_duration: float | int = Form(config.DEFAULT_ANIMATION_DURATION),
) -> dict:
    order_id = str(uuid.uuid4())
    order = {
            "order_id": order_id,
            "background_file": AssetFile(
                background_file.file.read(), background_file.filename.split(".")[-1]
            ),
            "foreground_file": (
                AssetFile(
                    foreground_file.file.read(), foreground_file.filename.split(".")[-1]
                )
                if foreground_file
                else None
            ),
            "audio_file": (
                AssetFile(audio_file.file.read(), audio_file.filename.split(".")[-1])
                if audio_file
                else None
            ),
            "quote_enabled": True if quote_text else False,
            "quote_text": quote_text,
            "quote_author_enabled": True if quote_author_text else False,
            "quote_author_text": quote_author_text,
            "template": template,
            "framerate": framerate,
            "audio_offset": audio_offset,
            "videogfx_tail": videogfx_tail,
            "animation_duration": animation_duration,
        }
    pprint(order)
    queue.append(order)
    queue.start_processing()
    return {"order_id": str(order_id)}


# videogfx server
app.mount(
    "/",
    StaticFiles(directory=Path.cwd().resolve()),
    name="static",
)
