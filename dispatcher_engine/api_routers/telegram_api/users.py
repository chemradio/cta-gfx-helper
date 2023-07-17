from fastapi import APIRouter, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from db_tortoise.helper_enums import NormalUserPermission
from db_tortoise.users_models import User, User_Pydantic


class TelegramUserIn(BaseModel):
    telegram_id: int
    first_name: str | None = None


router = APIRouter()


@router.get("/")
async def check_user_status(user: TelegramUserIn):
    user_db = await User.filter(telegram_id=user.telegram_id).first()
    if user_db is None:
        # print("user is not registered")
        raise HTTPException(404, "User is not registered")

    user_pydantic = await User_Pydantic.from_tortoise_orm(user_db)
    user_pydantic_jsonable = jsonable_encoder(user_pydantic)

    return user_pydantic_jsonable


@router.post("/")
async def register(
    # request: Request,
    user: TelegramUserIn,
):
    print(user)
    user_db = await User.filter(telegram_id=user.telegram_id).first()
    if user_db is not None:
        raise HTTPException(401, "User is already registered")

    user_db = await User.create(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        permission=NormalUserPermission.PENDING,
    )
    user_pydantic = await User_Pydantic.from_tortoise_orm(user_db)
    user_pydantic_jsonable = jsonable_encoder(user_pydantic)
    return user_pydantic_jsonable
