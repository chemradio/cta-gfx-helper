import json

from db_tortoise.users_models import User


async def get_all_users() -> list[User] | None:
    users = await User.all()
    if not users:
        return None
    return [user for user in users]


async def pythonize_users(users: list[dict] | None):
    if not users:
        return

    filtered_users = list()
    for user in users:
        target_fields = (
            "email",
            "role",
            "telegram_id",
            "first_name",
            "password_hash",
            "permission",
            "description",
            # "created",
            "username",
        )
        user_dict = dict(user)
        filtered_user_dict = {
            field: user_dict[field] for field in target_fields if field in user_dict
        }
        filtered_users.append(filtered_user_dict)

    return filtered_users


async def dump_backup(users: bool = True, orders: bool = True):
    update_dict = {"users": [], "orders": []}

    if users:
        users_tortoise = await get_all_users()
        pythonized_users = await pythonize_users(users_tortoise)
        update_dict["users"] = pythonized_users

    if orders:
        pass

    with open("seed.json", "wt") as seed_file:
        json.dump(update_dict, seed_file)
