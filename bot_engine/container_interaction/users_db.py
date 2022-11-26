import requests
from config import DISPATCHER_USERS_ENDPOINT, ADD_USER_ENDPOINT, EDIT_USER_ENDPOINT
from container_interaction.helpers import UserStatus


async def add_pending_user(user_dict: dict):
    user_dict.update({"status": "pending"})
    r = requests.post(ADD_USER_ENDPOINT, json=user_dict)


async def allow_user(telegram_id: int):
    r = requests.post(
        EDIT_USER_ENDPOINT, json={"telegram_id": telegram_id, "status": "allowed"}
    )


async def block_user(telegram_id: int):
    r = requests.post(
        EDIT_USER_ENDPOINT, json={"telegram_id": telegram_id, "status": "blocked"}
    )


async def list_users(type: UserStatus) -> list:
    r = requests.get(f"{DISPATCHER_USERS_ENDPOINT}/list", json={"status": type.value})
    json = r.json()
    return json["users"]


async def check_user_status(telegram_id: int) -> UserStatus:
    r = requests.get(
        f"{DISPATCHER_USERS_ENDPOINT}/checkStatus", json={"telegram_id": telegram_id}
    )
    return UserStatus(r.json()["status"])


# async def get_allowed_user_ids() -> list:
#     with open("token.txt", "r") as tf:
#         return [int(line) for line in tf.readlines()[1:]]


# async def get_blocked_user_ids() -> list:
#     return []


# async def get_pending_user_ids() -> list:
#     return []
