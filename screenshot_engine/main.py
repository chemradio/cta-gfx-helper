from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from pydantic.networks import AnyHttpUrl
from queue_manager.queue_manager import QueueManager
from screenshots.logic.controllers.auth_controller.cookie_manager.cookie_manager import (
    CookieManager,
)
from screenshots.logic.type_classes.screenshot import ScreenshotOrder


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

    order = ScreenshotOrder(
        screenshot_link=screenshot_link,
    )

    queue.append(order)
    background_tasks.add_task(queue.start_processing, operator=...)

    return order.to_dict()
