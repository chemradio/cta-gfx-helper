from fastapi import FastAPI, BackgroundTasks
from video_gfx.order_processor import process_video_gfx_orders


app = FastAPI()


@app.post("/start_video_gfx")
async def start_video_gfx(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_video_gfx_orders)
    return True
