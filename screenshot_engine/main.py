import config
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile
from queue_manager.queue_manager import QueueManager
from shared.orders.screenshot_order import ScreenshotOrder
from screenshots.order_processor import process_screenshot_order
from shared.api.file_server.api_input_classes import OrderCheck
from shared.api.file_server  import file_server_api
from shared.orders.screenshot_order import ScreenshotOrderIn
from shared.database.db import db_handler

queue = QueueManager()
app = FastAPI()
app.include_router(file_server_api.router)





@app.post("/")
async def capture_screenshots(
    screenshot_order: ScreenshotOrderIn,
    background_tasks: BackgroundTasks,
) -> dict:
    order = ScreenshotOrder(screenshot_link=screenshot_order.screenshot_link.__str__())
    db_handler.add_order(order)
    queue.append(order)
    background_tasks.add_task(queue.start_processing, operator=process_screenshot_order)
    return order.to_dict()


@app.get("/")
async def check_order_status(
    order: OrderCheck,
) -> dict:
    # return db_handler.get_order(order.order_id)
    ...


@app.post("/cookie_file")
async def create_cookie_file(upload_file: UploadFile):
    print("Request for storing cookie file.")
    with open(config.COOKIE_FILE, "wb") as f:
        f.write(upload_file.file.read())
    return "Cookie file stored."
