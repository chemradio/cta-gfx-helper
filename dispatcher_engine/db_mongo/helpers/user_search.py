from bson.objectid import ObjectId
from db_mongo.db_config.db_init import Users
from db_mongo.models.orders import Order
from db_mongo.models.users import User


def find_user(user: User | dict) -> User | None:
    if isinstance(user, dict):
        user = User(**user)
    # print(f"Searching for user... {user}, {type(user)=}")

    if user.email:
        query = {"email": user.email}
    elif user.telegram_id:
        query = {"telegram_id": user.telegram_id}
    elif user.id:
        print(user.id)
        query = {"_id": user.id}

    user_db = Users.find_one(query)
    # print(f"Search result: {user_db=}")
    if not user_db:
        return None
    return User(**user_db)


def find_user_by_order(order: Order | dict) -> User | None:
    if isinstance(order, dict):
        order = Order(**order)
    # print(f"Searching for user by order... {order}, {type(order)=}")
    if order.email:
        query = {"email": order.email}
    elif order.telegram_id:
        query = {"telegram_id": order.telegram_id}

    user_db = Users.find_one(query)
    if not user_db:
        return None
    # print(f"Search result: {user_db=}")
    return User(**user_db)
