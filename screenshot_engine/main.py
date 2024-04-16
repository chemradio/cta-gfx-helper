from fastapi import FastAPI, HTTPException, Depends, Body, BackgroundTasks
from pydantic.networks import AnyHttpUrl
from queue_manager.queue_manager import QueueManager

app = FastAPI()
queue = QueueManager()


@app.post("/")
async def capture_screenshots(
    background_tasks: BackgroundTasks,
    screenshot_link: AnyHttpUrl=Body(...),
):
    # if not secret_key:
    #     raise HTTPException(status_code=403, detail="Unauthorized request.")

    queue.append(screenshot_link)
    background_tasks.add_task(queue.start_processing, operator=...
                            #   time.sleep
                              )






# from screenshots.logic.controllers.auth_controller.cookie_manager.cookie_manager import (
#     CookieManager,
# )
# from screenshots.screenshot_order_processor import screenshooter_thread


# CookieManager.initialize_cookie_storage()


# function just as previous but with anyhttp url verificcation from the request body
# and secret key verification


# @app.get("/")
# async def get_screenshot_by_name(): ...


# @app.post("/cookie_file")
# async def replace_cookie_file(): ...
