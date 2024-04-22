from fastapi import FastAPI, HTTPException, Depends, Body, BackgroundTasks
from pydantic.networks import AnyHttpUrl
from queue_manager.queue_manager import QueueManager
from utils.generate_filename import generate_filename, ScreenshotFilenameType
from utils.generate_order_id import generate_order_id
from screenshots.logic.controllers.auth_controller.cookie_manager.cookie_manager import (
    CookieManager,
)

CookieManager.initialize_cookie_storage()
queue = QueueManager()

app = FastAPI()


@app.post("/")
async def capture_screenshots(
    background_tasks: BackgroundTasks,
    screenshot_link: AnyHttpUrl = Body(...),
):
    # if not secret_key:
    #     raise HTTPException(status_code=403, detail="Unauthorized request.")

    order = {
        "order_id": generate_order_id(),
        "screenshot_link": screenshot_link,
        "bg_filename": generate_filename(ScreenshotFilenameType.BACKGROUND),
        "fg_filename": generate_filename(ScreenshotFilenameType.FOREGROUND),
    }
    queue.append(order)
    background_tasks.add_task(queue.start_processing, operator=...)

    return order





# @app.get("/")
# async def get_screenshot_by_name(): ...


# @app.post("/cookie_file")
# async def replace_cookie_file(): ...
