from fastapi import APIRouter
from pymongo import ReturnDocument

from container_interaction.signal_sender import dispatch_to_microservices
from db_mongo.db_config.db_init import Orders
from db_mongo.models.orders import Order
from utils.order_logic.stage_increments import StageFlows

router = APIRouter()


@router.get("/")
async def get_one_intercontainer(filter: Order):
    print(f"Incoming filter: {filter=}")
    filter = {k: v for k, v in dict(filter).items() if v is not None}
    print(f"Search criteria: {filter=}")

    # fetch presend order
    order_db = Orders.find_one(filter)
    if not order_db:
        return None
    print(f"Found order: {order_db}")
    order = Order(**order_db)
    print(f"Converted order: {order}")

    # modify stage and save
    StageFlows.advance_stage(order)
    print(f"advanced order: {order}")

    Orders.update_one({"_id": order.id}, {"$set": dict(order)})
    print(f"after update")

    return order


@router.put("/", response_model=Order)
async def update_order(
    update: Order,
):
    # StageFlows.advance_stage(Order(order))
    print(f"Incoming update: {update=}")
    StageFlows.advance_stage(update)
    update_keys = (
        "error_type",
        "error",
        "error_type",
        "screenshots_ready",
        "is_two_layer",
        "video_gfx_ready",
        "current_stage",
    )
    update_data = {
        k: v for k, v in dict(update).items() if (v is not None) and (k in update_keys)
    }
    print(f"Updating order: {update_data}")
    order = Orders.find_one_and_update(
        {"_id": update.id},
        {"$set": update_data},
        return_document=ReturnDocument.AFTER,
    )
    await dispatch_to_microservices(Order(**order))
    return order
