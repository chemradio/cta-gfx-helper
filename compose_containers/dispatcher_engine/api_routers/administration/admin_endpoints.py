from fastapi import APIRouter, HTTPException
from db_mongo import Users, Orders, find_user
from pymongo import ReturnDocument

router = APIRouter()


@router.delete("/users")
async def delete_user(user_id: int):
    user = Users.find_one({"id": user_id})
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")

    Users.find_one_and_delete({"id": user_id})


@router.put("/users")
async def edit_user(user_id: int, fields: dict):
    user = Users.find_one({"id": user_id})
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")

    updated_user = Users.find_one_and_update(
        {"id": user_id}, {"$set": fields}, return_document=ReturnDocument.AFTER
    )
    return updated_user


@router.delete("/orders}")
async def delete_order(order_id: str):
    order = Orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(404, f"Ordder id {order_id} not found.")

    Orders.find_one_and_delete({"id": order_id})


@router.put("/orders")
async def edit_order(order_id: int, fields: dict):
    order = Orders.find_one({"id": order_id})
    if not order:
        raise HTTPException(404, f"Order id {order_id} not found.")

    updated_order = Orders.find_one_and_update(
        {"id": order_id}, {"$set": fields}, return_document=ReturnDocument.AFTER
    )
    return updated_order


@router.get("/users")
async def list_users(filters: dict | None):
    # in httpx use params=filters
    if filters:
        users_db = Users.find(filters)
    else:
        users_db = Users.find({})

    return [user for user in users_db]


@router.get("/orders")
async def list_orders(filters: dict | None):
    limit = filters.pop("limit", 10) if filters is not None else 10
    if filters:
        orders_db = Orders.find(filters).sort("created", -1).limit(limit)
    else:
        orders_db = Orders.find({}).sort("created", -1).limit(limit)

    output = list()
    for order in orders_db:
        user = find_user(order=order)
        order["user"] = user
        output.append(order)

    return output
