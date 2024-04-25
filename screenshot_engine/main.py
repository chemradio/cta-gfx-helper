import config
from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile
from fastapi.responses import FileResponse
from queue_manager.queue_manager import QueueManager
from screenshots.logic.type_classes.screenshot import ScreenshotOrder
from screenshots.order_processor import process_screenshot_order
from utils.api_pyclasses import (
    ScreenshotOrderIn,
    OrderCheck,
    FileRequest,
)
from utils.find_asset import find_asset

queue = QueueManager()
app = FastAPI()
db_handler = ...


@app.post("/")
async def capture_screenshots(
    screenshot_order: ScreenshotOrderIn,
    background_tasks: BackgroundTasks,
) -> dict:
    order = ScreenshotOrder(screenshot_link=screenshot_order.screenshot_link.__str__())
    queue.append(order)
    background_tasks.add_task(queue.start_processing, operator=process_screenshot_order)
    return order.to_dict()


@app.get("/")
async def check_order_status(
    order: OrderCheck,
) -> dict:
    # return db_handler.get_order(order.order_id)
    ...


@app.get("/file")
async def download_screenshot(file_request: FileRequest):
    file_path = find_asset(file_request.filename)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, "image/png", filename=file_path.name)


@app.delete("/file")
async def delete_screenshot(file_request: FileRequest):
    file_path = find_asset(file_request.filename)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    file_path.unlink()
    return {"status": "deleted", "filename": file_path.name}


@app.post("/cookie_file")
async def create_cookie_file(upload_file: UploadFile):
    print("Request for storing cookie file.")
    with open(config.COOKIE_FILE, "wb") as f:
        f.write(upload_file.file.read())
    return "Cookie file stored."
