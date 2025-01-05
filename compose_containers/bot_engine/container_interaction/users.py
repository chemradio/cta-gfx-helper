import os
import httpx

from config import USERS_ENDPOINT, ADMIN_USERS_ENDPOINT
from py_gfxhelper_lib.user_enums.user_permission import UserPermission
from py_gfxhelper_lib.user_enums.user_role import UserRole

async def add_pending_user(user_data: dict) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            USERS_ENDPOINT,
            json={**user_data, "permission": UserPermission.PENDING.value},
        )
        r.raise_for_status()
        return r.json()


async def get_user_data(telegram_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{USERS_ENDPOINT}", json={"telegram_id": telegram_id})
        r.raise_for_status()
        return r.json()


async def allow_user(telegram_id: int):
    user_db_id = await get_user_data(telegram_id).pop("id")
    async with httpx.AsyncClient() as client:
        r = await client.put(
            ADMIN_USERS_ENDPOINT,
            json={
                "user_id": user_db_id,
                "fields": {"permission": UserPermission.APPROVED.value},
            },
        )
        r.raise_for_status()
        return r.json()


async def pend_user(telegram_id: int):
    user_db_id = await get_user_data(telegram_id).pop("id")
    async with httpx.AsyncClient() as client:
        r = await client.put(
            ADMIN_USERS_ENDPOINT,
            json={
                "user_id": user_db_id,
                "fields": {"permission": UserPermission.PENDING.value},
            },
        )
        r.raise_for_status()
        return r.json()


async def block_user(telegram_id: int):
    user_db_id = await get_user_data(telegram_id).pop("id")
    async with httpx.AsyncClient() as client:
        r = await client.put(
            ADMIN_USERS_ENDPOINT,
            json={
                "user_id": user_db_id,
                "fields": {"permission": UserPermission.BLOCKED.value},
            },
        )
        r.raise_for_status()
        return r.json()


async def check_user_status(telegram_id: int) -> UserPermission:
    try:
        user_data = await get_user_data(telegram_id)
        return UserPermission(user_data.get("permission"))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return UserPermission.UNREGISTERED
    except Exception as e:
        print(f"Error: {e}")
        return UserPermission.UNREGISTERED


async def check_user_role(telegram_id: int) -> UserRole:
    try:
        user_data = await get_user_data(telegram_id)
        return UserRole(user_data.get("role"))
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError("User not found")
    except Exception as e:
        raise ValueError(f"Error: {e}")


async def check_user_role_admin(telegram_id: int) -> bool:
    return True if telegram_id == int(os.getenv("BOT_ADMIN")) else False


async def fetch_users(permission: UserPermission | None = None) -> list:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{USERS_ENDPOINT}/list/",
            json={"permission": permission.value} if permission else {},
        )
    return r.json()
