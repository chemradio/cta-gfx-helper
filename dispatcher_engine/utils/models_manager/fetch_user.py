from db_tortoise.orders_models import Order, Order_Pydantic
from db_tortoise.users_models import User, User_Pydantic


async def prefetch_user(order: Order) -> User:
    await order.fetch_related("user")
    return order.user


async def combine_order_user_dict(order: Order, user: User) -> dict:
    single_order_pydantic = await Order_Pydantic.from_tortoise_orm(order)
    single_user_pydantic = await User_Pydantic.from_tortoise_orm(user)
    order_dict = single_order_pydantic.dict()
    order_dict.update({"user": single_user_pydantic.dict()})
    return order_dict
