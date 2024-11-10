from datetime import datetime

from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from pymongo import ReturnDocument

from custom_types_enums import NormalUserPermission
from db_mongo.db_config.db_init import Users
from db_mongo.helpers.user_search import find_user
from db_mongo.models.users import User

router = APIRouter()


@router.get("/", response_model=User)
async def check_user_in_db(user: User):
    user_db = find_user(user)
    if user_db is None:
        raise HTTPException(404, "User is not registered")
    return user_db


@router.get("/list/", response_model=list[User])
async def list_users(permission: NormalUserPermission | None = None):
    users = Users.find({"permission": permission} if permission else None)
    return list(users)


@router.post("/", response_model=User)
async def register(user: User):
    existing_user = find_user(user)
    if existing_user is not None:
        raise HTTPException(401, "User is already registered")

    user_db_id = Users.insert_one(
        {**dict(user), "created": datetime.now().replace(microsecond=0).isoformat()}
    ).inserted_id
    return Users.find_one({"_id": ObjectId(user_db_id)})


@router.put("/", response_model=User)
async def edit_user(user: User):
    existing_user = find_user(user)
    if user is None:
        raise HTTPException(404, "User is not registered")

    update = {k: v for k, v in dict(user).items() if v is not None}
    updated_user = Users.find_one_and_update(
        {"_id": ObjectId(existing_user.id)},
        {"$set": update},
        return_document=ReturnDocument.AFTER,
    )
    return updated_user
