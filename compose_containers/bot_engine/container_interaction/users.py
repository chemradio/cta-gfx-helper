import httpx

from config import USERS_ENDPOINT
from py_gfxhelper_lib.user_enums import UserPermission, UserRole


async def get_user_data(telegram_id: int) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{USERS_ENDPOINT}", json={"telegram_id": telegram_id})
        if r.status_code == 404:
            return {}
        return r.json()


async def register_user(telegram_id: int, user_data: dict = {}) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            USERS_ENDPOINT,
            json={
                "telegram_id": telegram_id,
                "permission": UserPermission.PENDING.value,
                **user_data,
            },
        )
        r.raise_for_status()
        return r.json()


async def change_user_permission(telegram_id: int, permission: UserPermission):
    async with httpx.AsyncClient() as client:
        r = await client.put(
            USERS_ENDPOINT,
            json={
                "telegram_id": telegram_id,
                "update_data": {"permission": permission.value},
            },
        )
        r.raise_for_status()
        return r.json()


async def approve_user(telegram_id: int):
    return change_user_permission(telegram_id, UserPermission.APPROVED)


async def pend_user(telegram_id: int):
    return change_user_permission(telegram_id, UserPermission.PENDING)


async def block_user(telegram_id: int):
    return change_user_permission(telegram_id, UserPermission.BLOCKED)


async def get_user_permission(telegram_id: int) -> UserPermission:
    user_data = await get_user_data(telegram_id)
    if not user_data:
        return UserPermission.UNREGISTERED
    return UserPermission(user_data.get("permission"))


async def get_user_role(telegram_id: int) -> UserRole | None:
    user_data = await get_user_data(telegram_id)
    if not user_data:
        return None
    return UserRole(user_data.get("role"))


async def fetch_users(permission: UserPermission | None = None) -> list:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{USERS_ENDPOINT}/list/",
            json={"permission": permission.value} if permission else {},
        )
    return r.json()
