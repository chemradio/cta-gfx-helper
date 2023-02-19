from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from db.sql_handler import db
from processors.password_hashing import (
    PasswordVerificationFailed,
    generate_password_hash,
    verify_password,
)
from processors.token_manupulation import decode_jwt_payload, generate_jwt_token
from processors.vitaly_converters import vitaly_user_converter

router = APIRouter()


@router.post("/sessions")
async def login(request: Request):
    jwt_cookie = request.cookies.get("jwt")
    if jwt_cookie:
        try:
            user = decode_jwt_payload(jwt_cookie)
            response = JSONResponse(content=user)
            return response
        except:
            raise HTTPException(401, detail="Cookie verification failed")

    json_data: dict = await request.json()
    email = json_data.get("email")
    password = json_data.get("password")
    # username = json_data.get("username")

    user = db.find_user_by_email(email)
    if not user:
        raise HTTPException(401, detail="User is missing from the database")

    try:
        verify_password(password, user.password_hash)
    except PasswordVerificationFailed:
        raise HTTPException(401, detail="Wrong credentials")

    user_dict = user.to_dict()
    user_dict.pop("password_hash")
    user_dict = vitaly_user_converter(user_dict)
    access_token = generate_jwt_token(user_dict)

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "token_expiry": 60 * 60,
        }
    )
    response.set_cookie(key="jwt", value=f"Bearer {access_token}")
    return response


@router.delete("/sessions")
async def logout(request: Request):
    return True


@router.post("/")
async def register(request: Request):
    json_data: dict = await request.json()
    email = json_data["email"]
    password = json_data["password"]
    username = json_data["username"]

    if db.find_user_by_email(email):
        raise HTTPException(
            400, "User with such email is already present in the database"
        )

    user = db.add_user(
        email=email, password_hash=generate_password_hash(password), username=username
    )
    user_dict = user.to_dict()
    user_dict.pop("password_hash")
    user_dict = vitaly_user_converter(user_dict)
    access_token = generate_jwt_token(user_dict)

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
            "token_expiry": 60 * 60,
        }
    )
    response.set_cookie(key="jwt", value=f"Bearer {access_token}")
    return response
