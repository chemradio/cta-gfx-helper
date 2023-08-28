import os

import requests

from config import DISPATCHER_USERS_ENDPOINT, EDIT_USER_ENDPOINT, LIST_USERS_ENDPOINT
from container_interaction.helpers import UserPermission, UserRole


async def add_pending_user(user_dict: dict):
    print("posting")
    try:
        r = requests.post(DISPATCHER_USERS_ENDPOINT, json=user_dict)
    except:
        print("bad")


async def allow_user(telegram_id: int):
    r = requests.put(
        f"{EDIT_USER_ENDPOINT}/{telegram_id}",
        json={"permission": UserPermission.APPROVED.value},
    )
    return r.json()


async def pend_user(telegram_id: int):
    r = requests.put(
        f"{EDIT_USER_ENDPOINT}/{telegram_id}",
        json={"permission": UserPermission.PENDING.value},
    )
    return r.json()


async def block_user(telegram_id: int):
    r = requests.put(
        f"{EDIT_USER_ENDPOINT}/{telegram_id}",
        json={"permission": UserPermission.BLOCKED.value},
    )
    return r.json()


async def fetch_users(type: UserPermission | None = None) -> list:
    r = requests.get(
        LIST_USERS_ENDPOINT, json={"status": type.value} if type is not None else {}
    )
    return r.json()


async def check_user_status(telegram_id: int) -> UserPermission:
    r = requests.get(f"{DISPATCHER_USERS_ENDPOINT}", json={"telegram_id": telegram_id})
    if r.status_code == 404:
        return UserPermission.UNREGISTERED

    return UserPermission(r.json().get("permission"))


async def check_user_role(telegram_id: int) -> UserRole:
    r = requests.get(f"{DISPATCHER_USERS_ENDPOINT}", json={"telegram_id": telegram_id})
    if r.status_code == 404:
        return UserPermission.UNREGISTERED

    return UserRole(r.json().get("role"))


async def check_user_role_admin(telegram_id: int) -> bool:
    return True if telegram_id == int(os.getenv("BOT_ADMIN")) else False


async def get_user_data(telegram_id: int) -> dict:
    r = requests.get(f"{DISPATCHER_USERS_ENDPOINT}", json={"telegram_id": telegram_id})
    if r.status_code == 404:
        return None

    return r.json()
