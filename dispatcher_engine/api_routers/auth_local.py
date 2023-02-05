from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api_routers.oauth2_scheme import oauth2_scheme
from db.sql_handler import db
from processors.password_hashing import (
    PasswordVerificationFailed,
    generate_password_hash,
    verify_password,
)
from processors.token_manupulation import decode_jwt_payload, generate_jwt_token

router = APIRouter()


@router.post("/register")
def register_new_user(email: str = Form(), password: str = Form()):
    first_name = email.split("@")[0]
    try:
        db.add_user(
            first_name=first_name,
            email=email,
            password=generate_password_hash(password),
            status="allowed",
        )
        return True
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error occured: {e}")


@router.post("/token")
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username  # this is email btw
    password = form_data.password
    user = db.find_user_by_email(email=username)

    # check if user in db
    if not user:
        raise HTTPException(
            status_code=401, detail="User is not present in the database"
        )

    # check password
    try:
        verify_password(password, user.password_hash)
    except PasswordVerificationFailed:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    payload = {"username": username, "generated_at": "fastapi"}
    token = generate_jwt_token(payload)
    return {"access_token": token, "token_type": "bearer"}


@router.delete("/token")
def logout_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_payload(token)
    return payload
    ...
