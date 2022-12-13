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


async def block_user(telegram_id: int):
    r = requests.post(
        EDIT_USER_ENDPOINT, json={"telegram_id": telegram_id, "status": "blocked"}
    )


async def list_users(type: UserStatus) -> list:
    r = requests.get(f"{DISPATCHER_USERS_ENDPOINT}/list", json={"status": type.value})
    json = r.json()
    return json["users"]


async def check_user_status(telegram_id: int) -> UserStatus:
    print("entered check user status")
    r = requests.get(
        f"{DISPATCHER_USERS_ENDPOINT}/check_status", json={"telegram_id": telegram_id}
    )
    print("after_request check user status")

    result = r.json()
    print(f"return is {result}")

    if not result:
        print("not result f")
        user_status_string = "unregistered"
    else:
        user_status_string = result.get("status")

    print(f"{user_status_string=}")
    user_status = UserStatus(user_status_string)
    print(f"{user_status=}")

    return user_status
