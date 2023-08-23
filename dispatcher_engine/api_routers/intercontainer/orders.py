from pprint import pprint

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel

from container_interaction.signal_sender import signal_to_services
from db_tortoise.order_controller import OrderController
from db_tortoise.orders_models import Order, Order_Pydantic
from utils.models_manager.fetch_user import combine_order_user_dict
from utils.request_json_parser import request_json_parser

router = APIRouter()


class IntercontainerOrder_GetOne(BaseModel):
    current_stage: str
    status: str | None = "active"
    ordered_from: str | None = None


@router.put("/")
async def edit_order_intercontainer(
    background_tasks: BackgroundTasks,
    order_json: dict | None = Depends(request_json_parser),
):
    if not order_json:
        raise HTTPException(400, "Request body could not be parsed.")
    print(order_json)
    order_db = await Order.filter(id=order_json["id"]).first()

    update_keys = (
        "error_type",
        "error",
        "error_type",
        "screenshots_ready",
        "is_two_layer",
        "video_gfx_ready",
    )
    update_dict = {key: order_json[key] for key in update_keys if key in order_json}

    order_db = order_db.update_from_dict(update_dict)
    pprint(f"pre order advance: {dict(order_db)}")
    await order_db.save()
    await order_db.refresh_from_db()
    pprint(f"refresh order: {dict(order_db)}")
    await OrderController.advance_order_stage(order_db)
    await order_db.save()
    pprint(f"after order advance: {dict(order_db)}")

    # await order_db.refresh_from_db()
    # pprint(f"refresh order: {dict(order_db)}")
    # await OrderController.advance_order_stage(order_db)
    # await order_db.save()
    # pprint(f"after order advance: {dict(order_db)}")

    if order_db.status == "completed":
        # order completed
        # cleanup_order_assets(order_db)
        pass

    background_tasks.add_task(signal_to_services, order_db)
    return None


@router.get("/")
async def get_one_intercontainer(order: IntercontainerOrder_GetOne):
    order_db = await Order.filter(
        current_stage=order.current_stage,
        status=order.status,
        # ordered_from="web" if order.ordered_from is None else order.ordered_from,
    ).first()
    if not order_db:
        return None

    order_pydantic = await Order_Pydantic.from_tortoise_orm(order_db)
    await OrderController.advance_order_stage(order_db)
    await order_db.save()
    return order_pydantic
