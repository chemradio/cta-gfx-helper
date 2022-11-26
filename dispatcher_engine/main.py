from fastapi import FastAPI, BackgroundTasks
from db.sql_handler import SQLHandler
from container_interation.screenshoter import signal_to_screenshoter
from container_interation.video_gfx import signal_to_video_gfx
from container_interation.sender import signal_to_sender
import config
import time

time.sleep(10)
app = FastAPI()
db = SQLHandler()
db.recreate_tables()
db.init_add_admin()


@app.get("/")
def read_root():
    """Unused at the moment"""
    return {"Hello": "World"}


# users
@app.post("/users/add")
def add_user(user_dict: dict):
    db.add_user(**user_dict)
    return True


@app.post("/users/edit")
def edit_user(user_dict: dict):
    telegram_id = user_dict.pop("telegram_id")
    db.edit_user(telegram_id=telegram_id, **user_dict)
    return True


@app.get("/users/list")
def list_users(type: dict):
    """Returns a list of all users if not specified."""
    status_type = type.get("status")
    users = db.list_users(status_type)
    return {"users": users}


# orders
@app.post("/orders/add")
def add_order(order_dict: dict, background_tasks: BackgroundTasks):
    """Adds order to the database. Signals to other workers as needed."""
    print(f"{__name__}:{order_dict=}")
    request_type = order_dict.get("request_type")

    if request_type in ["only_screenshots", "video_auto"]:
        status = "screenshots_pending"
    else:
        status = "video_gfx_pending"

    render_output_path = (
        config.RENDER_OUTPUT_PATH / f"{str(request_type)}-gfx-{int(time.time())}.mp4"
    )
    order_dict.update({"status": status, "render_output_path": str(render_output_path)})

    # order_id = db.add_order(**order_dict)
    db.add_order(**order_dict)
    # order_dict.update({"order_id": order_id})

    match status:
        case "screenshots_pending":
            background_tasks.add_task(signal_to_screenshoter)
        case "video_gfx_pending":
            background_tasks.add_task(signal_to_video_gfx)
        case _:
            return False

    # if request_type in ["video_auto", "only_screenshots"]:
    #     background_tasks.add_task(signal_to_screenshoter)
    # if request_type == "video_files":
    #     background_tasks.add_task(signal_to_video_gfx)
    return True


@app.post("/orders/edit")
def edit_order(order_dict: dict, background_tasks: BackgroundTasks):
    order_id = order_dict.pop("order_id")
    if not db.edit_order(order_id=order_id, **order_dict):
        return False

    status = order_dict["status"]
    match status:
        case "ready_to_send":
            background_tasks.add_task(signal_to_sender)
        case "video_gfx_pending":
            background_tasks.add_task(signal_to_video_gfx)
        case _:
            return False
    return True


@app.post("/orders/truncate")
def truncate_orders():
    db.truncate_orders()
    return True


@app.get("/orders/list")
async def list_orders(type: dict):
    """Returns a list of all users if not specified."""
    status_type = type.get("status")
    orders = db.list_orders(status_type)
    return {"orders": orders}


@app.get("/orders/list_unsent_orders")
def list_unsent_orders():
    """Returns a list of unsent orders."""
    orders = db.list_orders("ready_to_send")
    return {"orders": orders}


@app.get("/orders/get_one")
async def get_one(type: dict):
    """Returns a list of all users if not specified."""
    status_type = type.get("status")
    orders = db.list_orders(status_type)
    if not orders:
        return {}
    return orders[0]


# @app.post("/orders/screenshots")
# def add_order(order: dict):
#     """Adds order to the database. Signals to other workers as needed."""
#     return True


# @app.get("/orders/active")
# def get_active_orders():
#     """Returns a list of active orders."""
#     return {"Hello": "World"}


# @app.get("/orders/processing")
# def get_processing_orders():
#     """Returns a list of the orders that are being processed."""
#     return {"Hello": "World"}
