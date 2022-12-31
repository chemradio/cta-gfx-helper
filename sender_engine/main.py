from fastapi import BackgroundTasks, FastAPI

from create_volume_folders import create_volume_folders
from send_process.orders_sender import orders_sender

create_volume_folders()

app = FastAPI()


@app.post("/send_orders")
async def send_orders(background_tasks: BackgroundTasks):
    background_tasks.add_task(orders_sender)
    return True
