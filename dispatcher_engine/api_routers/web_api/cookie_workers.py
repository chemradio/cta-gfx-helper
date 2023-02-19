from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from db.sql_handler import db
from db.sqlalchemy_models import User
from processors.password_hashing import (
    PasswordVerificationFailed,
    generate_password_hash,
    verify_password,
)
from processors.token_manupulation import decode_jwt_payload, generate_jwt_token
from processors.vitaly_converters import vitaly_user_converter


class CookieNotFound(Exception):
    ...


def verify_cookie(request: Request):
    # if already logged in
    jwt_cookie = request.cookies.get("jwt")
    if jwt_cookie:
        try:
            user = decode_jwt_payload(jwt_cookie)
            print("found cookie")
            print(f'{request.cookies.get("jwt")=}')
            response = JSONResponse(content=user)
            return response
        except:
            raise HTTPException(401, detail="Cookie verification failed")
    else:
        raise CookieNotFound()


def generate_cookie(user: User):
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
