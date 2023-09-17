from create_volume_folders import create_volume_folders
from fastapi import FastAPI
from send_process.orders_sender import orders_sender_raw, orders_sender_thread_raw

create_volume_folders()

app = FastAPI()


@app.post("/send_orders")
async def send_orders():
    orders_sender_thread_raw()
    return True
