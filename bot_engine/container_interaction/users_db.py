import os

import requests

from config import DISPATCHER_USERS_ENDPOINT, EDIT_USER_ENDPOINT, LIST_USERS_ENDPOINT
from telegram_bot.custom_types.user_permission_role import UserPermission, UserRole


async def add_pending_user(user_dict: dict):
    try:
        r = requests.post(
            DISPATCHER_USERS_ENDPOINT,
            json={**user_dict, "permission": UserPermission.PENDING.value},
        )
    except:
        print("bad")


async def allow_user(telegram_id: int):
    r = requests.put(
        DISPATCHER_USERS_ENDPOINT,
        json={
            "telegram_id": telegram_id,
            "permission": UserPermission.APPROVED.value,
            "role": UserRole.NORMAL.value,
        },
    )
    return r.json()


async def pend_user(telegram_id: int):
    r = requests.put(
        DISPATCHER_USERS_ENDPOINT,
        json={
            "telegram_id": telegram_id,
            "permission": UserPermission.PENDING.value,
            "role": UserRole.NORMAL.value,
        },
    )
    return r.json()


async def block_user(telegram_id: int):
    r = requests.put(
        DISPATCHER_USERS_ENDPOINT,
        json={
            "telegram_id": telegram_id,
            "permission": UserPermission.BLOCKED.value,
            "role": UserRole.NORMAL.value,
        },
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


async def fetch_users(permission: UserPermission | None = None) -> list:
    r = requests.get(
        f"{DISPATCHER_USERS_ENDPOINT}/list/",
        json={"permission": permission.value} if permission is not None else {},
    )
    print(f"Fetched users: {r.json()}", flush=True)
    return r.json()
