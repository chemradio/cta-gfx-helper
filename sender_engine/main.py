from fastapi import FastAPI, BackgroundTasks
from send_process.orders_sender import orders_sender

app = FastAPI()


@app.post("/send_orders")
def send_orders(background_tasks: BackgroundTasks):
    background_tasks.add_task(orders_sender)
    return True
