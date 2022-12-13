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
    print("pre request is admin")
    r = requests.get(
        f"{DISPATCHER_USERS_ENDPOINT}/check_status", json={"telegram_id": telegram_id}
    )
    print("post request is admin")
    print(f"json is {r.json()}")
    print(f'return is {UserStatus(r.json()["status"])}')

    return UserStatus(r.json()["status"])
