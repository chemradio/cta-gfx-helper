import asyncio
from datetime import datetime

from bson.objectid import ObjectId
from fastapi import APIRouter

from db_mongo.db_config.db_init import Orders
from db_mongo.helpers.user_search import find_user_by_order
from db_mongo.models.orders import Order
from order_processor.order_processor import process_order

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
    order.telegram_id = user.telegram_id

    # save order in db
    order_db_id = Orders.insert_one(
        {**dict(order), "created": datetime.now().replace(microsecond=0).isoformat()}
    ).inserted_id
    order = Orders.find_one({"_id": ObjectId(order_db_id)})

    asyncio.create_task(process_order(order.dict()))
    return order


@router.put("/", response_model=Order)
async def update_order(
    update: Order,
):
    order = Orders.find_one_and_update({"_id": update.id}, {"$set": dict(update)})
    return order
