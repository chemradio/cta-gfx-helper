import requests

from config import ADD_USER_ENDPOINT, DISPATCHER_USERS_ENDPOINT, EDIT_USER_ENDPOINT
from container_interaction.helpers import UserStatus


async def add_pending_user(user_dict: dict):
    user_dict.update({"status": "pending"})
    r = requests.post(ADD_USER_ENDPOINT, json=user_dict)


async def allow_user(telegram_id: int):
    r = requests.post(
        EDIT_USER_ENDPOINT, json={"telegram_id": telegram_id, "status": "allowed"}
    )


async def pend_user(telegram_id: int):
    r = requests.post(
        EDIT_USER_ENDPOINT, json={"telegram_id": telegram_id, "status": "pending"}
    )


async def block_user(telegram_id: int):
    r = requests.post(
        EDIT_USER_ENDPOINT, json={"telegram_id": telegram_id, "status": "blocked"}
    )


async def fetch_users(type: UserStatus = UserStatus.ALL) -> list:
    r = requests.get(f"{DISPATCHER_USERS_ENDPOINT}/list", json={"status": type.value})
    json = r.json()
    return json["users"]


async def check_user_status(telegram_id: int) -> UserStatus:
    r = requests.get(
        f"{DISPATCHER_USERS_ENDPOINT}/check_status", json={"telegram_id": telegram_id}
    )
    result = r.json()
    if not result:
        print("not result f")
        user_status_string = "unregistered"
    else:
        user_status_string = result.get("status")
    user_status = UserStatus(user_status_string)
    return user_status
