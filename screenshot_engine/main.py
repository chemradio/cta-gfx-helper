from fastapi import FastAPI, BackgroundTasks
from screenshots.screenshot_order_processor import process_screenshot_orders

app = FastAPI()


@app.post("/start_screenshoting")
async def start_screenshooting(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_screenshot_orders)
    return True
