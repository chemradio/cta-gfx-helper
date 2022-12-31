from fastapi import APIRouter, BackgroundTasks

from api_routers.signal_sender import signal_to_services
from db.sql_handler import db
from processors.orders import advance_order_stage

router = APIRouter()

# orders
@router.post("/add")
def add_order(order: dict, background_tasks: BackgroundTasks):
    order = advance_order_stage(order)
    db.add_order(**order)
    background_tasks.add_task(signal_to_services, order.get("current_stage"))
    return True


@router.post("/edit")
def edit_order(order: dict, background_tasks: BackgroundTasks):
    order = advance_order_stage(order)
    if not db.edit_order(**order):
        return False

    current_stage = order.get("current_stage")
    background_tasks.add_task(signal_to_services, current_stage)
    return True


@router.post("/truncate")
def truncate_orders():
    db.truncate_orders()
    return True


@router.get("/list")
def list_orders(request: dict = {}):
    """Returns a list of all orders if not specified."""
    status = request.get("status")
    orders = db.list_orders(status)

    for order in orders:
        user = db.find_user_by_telegram_id(order.user_telegram_id)
        order.user_first_name = user.first_name

    return {"orders": orders}


@router.get("/get_one")
def get_one(request: dict):
    """Returns a list of all users if not specified."""
    current_stage = request.get("current_stage")

    request_status = request.get("status")
    status = request_status if request_status else "active"

    order = db.get_one_order(current_stage, status)
    if not order:
        return None

    # generate and cleanup the order dict
    order_dict = order.__dict__
    order_dict.pop("_sa_instance_state")

    updated_order = advance_order_stage(order_dict)
    db.edit_order(**updated_order)

    return order
