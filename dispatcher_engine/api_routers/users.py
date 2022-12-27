from fastapi import APIRouter
from db.sql_handler import db

router = APIRouter()

# users
@router.post("/users/add")
async def add_user(user_dict: dict):
    db.add_user(**user_dict)
    return True


@router.get("/users/check_status")
async def check_user_status(user_dict: dict):
    telegram_id = user_dict.pop("telegram_id")
    user = db.find_user_by_telegram_id(telegram_id)
    if not user:
        return False
    return {"status": user.status}


@router.post("/users/edit")
async def edit_user(user_dict: dict):
    telegram_id = user_dict.pop("telegram_id")
    db.edit_user(telegram_id=telegram_id, **user_dict)
    return True


@router.get("/users/list")
async def list_users(type: dict):
    """Returns a list of all users if not specified."""
    status_type = type.get("status")
    if not status_type or (status_type == "all"):
        status_type = None

    users = db.list_users(status_type)
    return {"users": users}
