from datetime import datetime
from typing import List

from bson.objectid import ObjectId
from fastapi import APIRouter

from container_interaction.signal_sender import dispatch_to_microservices
from db_mongo.db_config.db_init import Orders
from db_mongo.helpers.user_search import find_user_by_order
from db_mongo.models.orders import Order
from utils.order_logic.new_order_actions import assign_filenames
from utils.order_logic.stage_increments import StageFlows

router = APIRouter()


@router.get("/")
async def list_orders(
    filter: Order | None = {},
) -> list[Order]:
    filter = {k: v for k, v in dict(filter).items() if v is not None and k is not "id"}
    orders = Orders.find(filter)
    return list(orders)


@router.post("/", response_model=Order)
async def add_new_order(
    order: Order,
):
    user = find_user_by_order(order)
    order.user_id = user.id

    # fix quote and audio fields
    order.quote_enabled = True if order.quote_text else False
    order.quote_author_enabled = True if order.quote_author_text else False
    order.audio_enabled = True if order.audio_name else False

    # assign filenames and advance stage
    assign_filenames(order)
    StageFlows.advance_stage(order)

    # save order in db
    order_db_id = Orders.insert_one(
        {**dict(order), "created": datetime.now().replace(microsecond=0).isoformat()}
    ).inserted_id
    order = Orders.find_one({"_id": ObjectId(order_db_id)})

    await dispatch_to_microservices(Order(**order))
    return order


@router.put("/", response_model=Order)
async def update_order(
    update: Order,
):
    order = Orders.find_one_and_update({"_id": update.id}, {"$set": dict(update)})
    return order
