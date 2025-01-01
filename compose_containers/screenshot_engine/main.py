import uuid

from fastapi import FastAPI, Form, UploadFile

import config
from src import main_capture
from src.driver_auth import initialize_cookie_storage
from py_gfxhelper_lib.startup import purge_storage
from py_gfxhelper_lib import QueueManager
from py_gfxhelper_lib.fastapi_routers import order_check_router, file_server_router
from py_gfxhelper_lib import DBHandler

DBHandler.init()

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
    db_handler=DBHandler,
)

app = FastAPI()
app.include_router(file_server_router)
app.include_router(order_check_router)

from py_gfxhelper_lib.fastapi_routers.order_check import get_db_handler

app.dependency_overrides[get_db_handler] = lambda: DBHandler


@app.post("/", response_model=dict)
async def capture_screenshots(
    screenshot_link: str = Form(None),
    callback_url: str | None = None,
) -> dict:
    order_id = str(uuid.uuid4())
    queue.append(
        {
            "order_id": order_id,
            "screenshot_link": screenshot_link,
            "callback_url": callback_url,
            "status": "new",
        }
    )
    queue.start_processing()
    return {"order_id": str(order_id)}


@app.post("/cookie_file")
async def create_cookie_file(upload_file: UploadFile):
    with open(config.COOKIE_FILE, "wb") as f:
        f.write(upload_file.file.read())
    return "Cookie file stored."
