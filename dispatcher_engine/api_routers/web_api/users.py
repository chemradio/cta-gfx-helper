from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from pydantic import EmailStr

from config import REGISTER_PASSPHRASE
from db_tortoise.helper_enums import NormalUserPermission
from db_tortoise.users_models import User, User_Pydantic, UserIn_Pydantic
from utils.auth.cookie_parser import cookie_parser
from utils.auth.jwt_cookie_response import generate_cookie_json_response
from utils.auth.password_hashing import (
    PasswordVerificationFailed,
    generate_password_hash,
    verify_password,
)

router = APIRouter()


@router.post("/")
async def register(
    email: EmailStr = Form(...),
    password: str = Form(...),
    passphrase: str = Form(...),
):
    # check if user already exists in database
    if await User.filter(email=email).first() is not None:
        raise HTTPException(401, "User with such email is already exists")

    # check the passphrase
    if (not passphrase) or passphrase != REGISTER_PASSPHRASE:
        raise HTTPException(401, detail="Passphrase incorrect or missing")

    # add user to db
    user_db = await User.create(
        email=email,
        password_hash=generate_password_hash(password),
        permission=NormalUserPermission.APPROVED.value
        if passphrase
        else NormalUserPermission.PENDING.value,
    )

    response = await generate_cookie_json_response(user_db)
    return response


@router.post("/sessions")
async def login(
    request: Request,
    user: UserIn_Pydantic | None = Depends(UserIn_Pydantic.as_form),
    user_cookie: User_Pydantic | None = Depends(cookie_parser),
):
    # check if already logged in
    print(user_cookie)
    if user_cookie:
        print("Correct cookie detected. Sending it back.")
        user_cookie_jsonable = jsonable_encoder(user_cookie)
        response = JSONResponse(content=user_cookie_jsonable)
        response.set_cookie(key="jwt", value=request.cookies.get("jwt"))
        return response

    print(user.dict())

    # check user in db
    print("checking if user is in db")
    user_db = await User.filter(email=user.email).first()
    if not user_db:
        raise HTTPException(401, detail="User is missing from the database")

    # verify user's password
    print("verifying password")
    try:
        verify_password(user.password, user_db.password_hash)
    except PasswordVerificationFailed:
        raise HTTPException(401, detail="Wrong credentials.")

    response = await generate_cookie_json_response(user_db)
    return response


@router.delete("/sessions")
async def logout(
    request: Request,
    response: Response,
    # request: Request,
    # user_cookie: User_Pydantic | None = Depends(cookie_parser),
):
    print(response)
    response.delete_cookie("jwt")
    return True


@router.get("/verify_token")
async def verify_token(
    token: User_Pydantic | None = Depends(cookie_parser),
):
    print("received token: ", token)
    user_cookie_jsonable = jsonable_encoder(token)
    response = JSONResponse(content=user_cookie_jsonable)
    return response
