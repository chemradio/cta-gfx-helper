from pprint import pprint

from container_interaction.signal_sender import signal_to_services
from db_tortoise.order_controller import OrderController
from db_tortoise.orders_models import Order, Order_Pydantic
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
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

    order_db = await Order.filter(id=order_json["id"]).first()

    # order_db.update_from_dict(
    #     {
    #         k: v
    #         for k, v in order_json.items()
    #         if k
    #         in (
    #             "error",
    #             "error_type",
    #             "screenshots_ready",
    #             "send_success",
    #             "video_gfx_ready",
    #         )
    #     }
    # )
    order = order_db.update_from_dict(order_json)
    pprint(f"pre order advance: {order_db=}")
    await order_db.refresh_from_db()
    await OrderController.advance_order_stage(order_db)
    await order_db.save()
    pprint(f"after order advance: {order_db=}")

    if order_db.status == "completed":
        # order completed
        # cleanup_order_assets(order_db)
        pass

    background_tasks.add_task(signal_to_services, order_db.current_stage)
    return None


@router.get("/")
async def get_one_intercontainer(order: IntercontainerOrder_GetOne):
    order_db = await Order.filter(
        current_stage=order.current_stage,
        status=order.status,
        ordered_from="web" if order.ordered_from is None else order.ordered_from,
    ).first()
    if not order_db:
        return None

    order_pydantic = await Order_Pydantic.from_tortoise_orm(order_db)
    await OrderController.advance_order_stage(order_db)
    await order_db.save()
    return order_pydantic
