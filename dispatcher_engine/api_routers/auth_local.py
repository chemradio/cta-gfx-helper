from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api_routers.oauth2_scheme import oauth2_scheme
from db.sql_handler import db
from processors.password_hashing import (
    PasswordVerificationFailed,
    generate_password_hash,
    verify_password,
)
from processors.token_manupulation import decode_jwt_payload, generate_jwt_token
from processors.vitaly_user_converter import vitaly_converter

router = APIRouter()


# @router.post("/register")
# def register_new_user(email: str = Form(), password: str = Form()):
#     first_name = email.split("@")[0]
#     try:
#         db.add_user(
#             first_name=first_name,
#             email=email,
#             password_hash=generate_password_hash(password),
#             status="allowed",
#         )
#     except Exception as e:
#         raise HTTPException(status_code=422, detail=f"Error occured: {e}")

#     payload = {"username": email, "generated_at": "fastapi"}
#     token = generate_jwt_token(payload)
#     return {"access_token": token, "token_type": "bearer"}


# @router.post("/token")
# def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     username = form_data.username  # this is email btw
#     password = form_data.password
#     user = db.find_user_by_email(email=username)

#     # check if user in db
#     if not user:
#         raise HTTPException(
#             status_code=401, detail="User is not present in the database"
#         )

#     # check password
#     try:
#         verify_password(password, user.password_hash)
#     except PasswordVerificationFailed:
#         raise HTTPException(status_code=400, detail="Invalid credentials")

#     payload = {"username": username, "generated_at": "fastapi"}
#     token = generate_jwt_token(payload)
#     return {"access_token": token, "token_type": "bearer"}


# @router.get("/token_verify")
# def confirm_authentication(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = decode_jwt_payload(token)
#         return payload
#     except:
#         raise HTTPException(status_code=401)


# @router.delete("/token")
# def logout_user(token: str = Depends(oauth2_scheme)):
#     payload = decode_jwt_payload(token)
#     return payload
#     ...


@router.post("/users/sessions")
async def login(request: Request):
    jwt_cookie = request.cookies.get("jwt")
    if jwt_cookie:
        user = decode_jwt_payload(jwt_cookie)
        print("found cookie")
        print(f'{request.cookies.get("jwt")=}')
        response = JSONResponse(content=user)
        return response

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
    user_dict = vitaly_converter(user_dict)
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


@router.delete("/users/sessions")
async def logout(request: Request):
    return True


@router.post("/users")
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
    user_dict = user.to_dict()
    user_dict.pop("password_hash")
    user_dict = vitaly_converter(user_dict)
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
