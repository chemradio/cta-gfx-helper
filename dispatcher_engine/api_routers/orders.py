from fastapi import APIRouter
from db.sql_handler import db
from fastapi import BackgroundTasks
import time
import config
from container_interation.screenshoter import signal_to_screenshoter
from container_interation.video_gfx import signal_to_video_gfx
from container_interation.sender import signal_to_sender

router = APIRouter()

# orders
@router.post("/orders/add")
async def add_order(order_dict: dict, background_tasks: BackgroundTasks):
    """Adds order to the database. Signals to other workers as needed."""
    print(f"{__name__}:{order_dict=}")
    request_type = order_dict.get("request_type")

    if request_type in ["only_screenshots", "video_auto"]:
        current_stage = "screenshots_pending"
    else:
        current_stage = "video_gfx_pending"

    render_output_path = (
        config.RENDER_OUTPUT_PATH / f"{str(request_type)}-gfx-{int(time.time())}.mp4"
    )
    order_dict.update(
        {
            "status": "active",
            "current_stage": current_stage,
            "render_output_path": str(render_output_path),
        }
    )

    db.add_order(**order_dict)

    match current_stage:
        case "screenshots_pending":
            background_tasks.add_task(signal_to_screenshoter)
        case "video_gfx_pending":
            background_tasks.add_task(signal_to_video_gfx)
        case _:
            return False

    return True


@router.post("/orders/edit")
async def edit_order(order_dict: dict, background_tasks: BackgroundTasks):
    order_id = order_dict.pop("order_id")
    if not db.edit_order(order_id=order_id, **order_dict):
        return False

    current_stage = order_dict["current_stage"]
    match current_stage:
        case "ready_to_send":
            background_tasks.add_task(signal_to_sender)
        case "video_gfx_pending":
            background_tasks.add_task(signal_to_video_gfx)
        case _:
            pass
    return True


@router.post("/orders/truncate")
async def truncate_orders():
    db.truncate_orders()
    return True


@router.get("/orders/list")
async def list_orders(status: dict = {}):
    """Returns a list of all orders if not specified."""
    status = status.get("status")
    orders = db.list_orders(status)

    for order in orders:
        user = db.find_user_by_telegram_id(order.user_telegram_id)
        order.user_first_name = user.first_name

    return {"orders": orders}


@router.get("/orders/get_one")
async def get_one(current_stage: dict, status: str = "active"):
    """Returns a list of all users if not specified."""
    current_stage = current_stage.get("current_stage")
    order = db.get_one_order(current_stage, status)
    return order if order else None
