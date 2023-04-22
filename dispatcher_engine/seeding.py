import json

from db_tortoise.helper_enums import NormalUserPermission
from db_tortoise.users_models import User
from utils.auth.password_hashing import generate_password_hash


async def seed_users(users: list[dict]):
    if not users:
        return None

    return_users = list()

    for user in users:
        user = await User.create(
            email=user.get("email"),
            password_hash=generate_password_hash(user.get("password")),
            permission=NormalUserPermission.APPROVED.value,
        )
        return_users.append(dict(user))

    return return_users


async def seed_orders(orders: list[dict]):
    return None


async def seed() -> dict[list]:
    with open("seed.json", "r") as f:
        seed_data: dict[list[dict]] = json.load(f)

    users_seeded = await seed_users(seed_data.get("users"))
    orders_seeded = await seed_orders(seed_data.get("orders"))

    return {"users": users_seeded, "orders": orders_seeded}
