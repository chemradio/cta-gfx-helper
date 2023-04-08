from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from container_interaction.signal_sender import signal_to_services
from db_tortoise.order_controller import OrderController
from db_tortoise.orders_models import Order, Order_Pydantic, OrderIn_Pydantic
from db_tortoise.users_models import User, User_Pydantic
from utils.auth.cookie_parser import cookie_parser

router = APIRouter()


# @router.post("/")
# async def add_order(
#     request: Request,
#     user_cookie: User_Pydantic | None = Depends(cookie_parser),
#     # order_in: OrderIn_Pydantic = Depends(OrderIn_Pydantic.as_form),
# ):
#     form_data = await request.body()
#     print(form_data)
#     return None


@router.post("/")
async def add_order(
    background_tasks: BackgroundTasks,
    user_cookie: User_Pydantic | None = Depends(cookie_parser),
    order_in: OrderIn_Pydantic = Depends(OrderIn_Pydantic.as_form),
):
    if not user_cookie:
        raise HTTPException(401, detail="Unauthorized")

    user = await User.filter(email=user_cookie.email).first()
    order_db = await Order(**order_in.dict(), user=user)

    order_db.quote_author_enabled = True if order_in.quote_author_text else False

    await OrderController.save_user_files(order_db)
    await OrderController.advance_order_stage(order_db)
    await order_db.save()
    await order_db.refresh_from_db()

    # background_tasks.add_task(signal_to_services, order_db.current_stage)
    return await Order_Pydantic.from_tortoise_orm(order_db)


@router.get("/")
async def get_user_active_orders(
    user_cookie: User_Pydantic | None = Depends(cookie_parser),
):
    """Returns all active orders from user in a form of a list of dicts."""
    if not user_cookie:
        raise HTTPException(401, detail="Unauthorized")

    user = await User.filter(email=user_cookie.email).first()

    orders_db = await Order.filter(status="active", user=user)
    orders_pydantic = [
        await Order_Pydantic.from_tortoise_orm(order_db) for order_db in orders_db
    ]
    return orders_pydantic
