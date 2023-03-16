from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response

from db_tortoise.users_models import User, User_Pydantic, UserIn_Pydantic
from utils.auth.cookie_parser import cookie_parser
from utils.auth.jwt_cookie_response import generate_cookie_json_response
from utils.auth.password_hashing import (
    PasswordVerificationFailed,
    generate_password_hash,
    verify_password,
)

router = APIRouter()


@router.post("/sessions")
async def login(
    user: UserIn_Pydantic | None = Depends(UserIn_Pydantic.as_form),
    user_cookie: User_Pydantic | None = Depends(cookie_parser),
):
    # check if already logged in
    if user_cookie:
        print("Correct cookie detected. Sending it back.")
        user_cookie_jsonable = jsonable_encoder(user_cookie)
        response = JSONResponse(content=user_cookie_jsonable)
        return response

    # check user in db
    user_db = await User.filter(email=user.email).first()
    if not user_db:
        raise HTTPException(401, detail="User is missing from the database")

    # verify user's password
    try:
        verify_password(user.password, user_db.password_hash)
    except PasswordVerificationFailed:
        raise HTTPException(401, detail="Wrong credentials.")

    response = await generate_cookie_json_response(user_db)
    return response


@router.delete("/sessions")
async def logout(
    response: Response,
    # request: Request,
    # user_cookie: User_Pydantic | None = Depends(cookie_parser),
):
    response.delete_cookie("jwt")
    return True


@router.post("/")
async def register(
    # request: Request,
    user: UserIn_Pydantic = Depends(UserIn_Pydantic.as_form),
    # user: UserIn_Pydantic,
):
    # check if user already exists in database
    if await User.filter(email=user.email).first() is not None:
        raise HTTPException(400, "User with such email is already exists.")

    # add user to db
    user_db = await User.create(
        email=user.email,
        password_hash=generate_password_hash(user.password),
        username=user.username,
    )

    response = await generate_cookie_json_response(user_db)
    return response
