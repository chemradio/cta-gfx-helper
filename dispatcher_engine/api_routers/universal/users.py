from datetime import datetime
from uuid import uuid4
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument

from custom_types_enums import NormalUserPermission
from db_mongo import find_user, Users

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
    return user_db


@router.post("/")
async def register(
    email: str | None = None,
    telegram_id: int | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    description: str | None = None,
):
    existing_user = find_user(email=email, telegram_id=telegram_id)
    if existing_user is not None:
        raise HTTPException(401, "User is already registered")

    user_db_id = Users.insert_one(
        {
            "id": str(uuid4()),
            "email": email,
            "telegram_id": telegram_id,
            "first_name": first_name,
            "last_name": last_name,
            "description": description,
            "permission": NormalUserPermission.PENDING,
            "created": datetime.now().replace(microsecond=0).isoformat(),
        }
    )
    return Users.find_one({"_id": ObjectId(user_db_id)})


@router.put("/")
async def edit_user(
    user_id: str | None = None,
    email: str | None = None,
    telegram_id: int | None = None,
    update_data: dict = None,
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
        return_document=ReturnDocument.AFTER,
    )
    return updated_user


@router.get("/list/")
async def list_users_by_permission(permission: NormalUserPermission | None = None):
    users = Users.find({"permission": permission} if permission else None)
    return list(users)
