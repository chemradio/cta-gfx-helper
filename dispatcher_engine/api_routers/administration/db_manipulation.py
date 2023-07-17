from fastapi import APIRouter, Depends, HTTPException

from db_tortoise.orders_models import Order, Order_Pydantic
from db_tortoise.users_models import User, User_Pydantic
from utils.request_json_parser import request_json_parser

router = APIRouter()


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    order = await Order.filter(id=order_id).first()
    if not order:
        raise HTTPException(404, f"Ordder id {order_id} not found.")
    await order.delete()
    return None


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")
    await user.delete()
    return None


@router.put("/users/{user_id}")
async def edit_user(user_id: int, fields: dict | None = Depends(request_json_parser)):
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(404, f"User id {user_id} not found.")

    try:
        user.update_from_dict(fields)
        await user.save()
        await user.refresh_from_db()
        return await User_Pydantic.from_tortoise_orm(user)
    except Exception as e:
        raise HTTPException(400, f"Error: {str(e)}")


@router.put("/users/telegram/{telegram_id}")
async def edit_user(
    telegram_id: int, fields: dict | None = Depends(request_json_parser)
):
    user = await User.filter(telegram_id=telegram_id).first()
    if not user:
        raise HTTPException(404, f"User {telegram_id} not found.")

    try:
        user.update_from_dict(fields)
        await user.save()
        await user.refresh_from_db()
        return await User_Pydantic.from_tortoise_orm(user)
    except Exception as e:
        raise HTTPException(400, f"Error: {str(e)}")


@router.put("/orders/{order_id}")
async def edit_order(order_id: int, fields: dict | None = Depends(request_json_parser)):
    order = await Order.filter(id=order_id).first()
    if not order:
        raise HTTPException(404, f"Order id {order_id} not found.")

    try:
        order.update_from_dict(fields)
        await order.save()
        await order.refresh_from_db()
        return await Order_Pydantic.from_tortoise_orm(order)
    except Exception as e:
        raise HTTPException(400, f"Error: {str(e)}")


@router.get("/users")
async def list_users(filters: dict | None = Depends(request_json_parser)):
    if filters:
        users_db = await User.filter(**filters).all()
    else:
        users_db = await User.all()

    orders_pydantic = [
        await User_Pydantic.from_tortoise_orm(user_db) for user_db in users_db
    ]
    return orders_pydantic


@router.get("/orders")
async def list_orders(filters: dict | None = Depends(request_json_parser)):
    if filters:
        orders_db = await Order.filter(**filters).all()
    else:
        orders_db = await Order.all()

    orders_pydantic = list()
    for order_db in orders_db:
        await order_db.fetch_related("user")
        single_order_pydantic = await Order_Pydantic.from_tortoise_orm(order_db)
        single_user_pydantic = await User_Pydantic.from_tortoise_orm(order_db.user)
        order_dict = single_order_pydantic.dict()
        order_dict.update({"user": single_user_pydantic.dict()})
        orders_pydantic.append(order_dict)
    return orders_pydantic
