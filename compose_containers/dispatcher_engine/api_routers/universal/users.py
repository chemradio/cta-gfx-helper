from uuid import uuid4
from fastapi import APIRouter, HTTPException, Body
import pymongo

from py_gfxhelper_lib.user_enums import UserPermission, UserRole
from db_mongo import find_user, Users
import time

router = APIRouter()


@router.get("/")
async def check_user_in_db(
    user_id: str | None = None,
    email: str | None = None,
    telegram_id: int | None = None,
):
    user_db = find_user(
        user_id=user_id,
        email=email,
        telegram_id=telegram_id,
    )
    if user_db is None:
        raise HTTPException(404, "User is not registered")
    user_db.pop("_id")
    return user_db


@router.post("/")
async def register(
    email: str | None = Body(None),
    telegram_id: int | None = Body(None),
    permission: UserPermission = Body(UserPermission.PENDING.value),
    role: UserRole = Body(UserRole.NORMAL.value),
    first_name: str | None = Body(None),
    last_name: str | None = Body(None),
    description: str | None = Body(None),
):
    print("register accessed")
    print(
        f"{email=}, {telegram_id=}, {permission=}, {role=}, {first_name=}, {last_name=}, {description=}"
    )

    print("searching for existing user")
    existing_user = find_user(email=email, telegram_id=telegram_id)
    print("existing_user", existing_user)
    if existing_user is not None:
        raise HTTPException(401, "User is already registered")

    user_id = str(uuid4())
    user_db_id = Users.insert_one(
        {
            "id": user_id,
            "email": email,
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
            "description": description,
            "permission": permission,
            "role": role,
            "created": int(time.time()),
        }
    )
    user_db = Users.find_one({"id": user_id})
    user_db.pop("_id")
    return user_db


@router.put("/")
async def edit_user(
    user_id: str | None = Body(None),
    email: str | None = Body(None),
    telegram_id: int | None = Body(None),
    update_data: dict = Body(None),
):
    user_db = find_user(
        user_id=user_id,
        email=email,
        telegram_id=telegram_id,
    )
    if user_db is None:
        raise HTTPException(404, "User is not registered")

    updated_user = Users.find_one_and_update(
        {"id": user_db["id"]},
        {"$set": update_data},
        return_document=pymongo.ReturnDocument.AFTER,
    )
    updated_user.pop("_id")
    return updated_user


@router.get("/list/")
async def list_users_by_permission(permission: UserPermission | None = None):
    users = Users.find({"permission": permission} if permission else {}).sort(
        "created", pymongo.DESCENDING
    )
    if not users:
        return []
    return [{k: v for k, v in user.items() if k != "_id"} for user in users]
