from fastapi import APIRouter
from db.sql_handler import db

router = APIRouter()


@router.get("/backup")
async def backup_db():
    "generates a json for database backup"
    # gather users
    users = db.list_users()
    orders = db.list_orders()
    return {"users": users, "orders": orders}


@router.post("/restore")
async def restore_db(backup: dict):
    "restores db to provided json"
    # old_state = backup_db()
    # return old_state

    # truncate db
    db.re_init_full_truncate()

    # add users
    users: dict[dict] = backup.get("users")
    for user in users:
        db.add_user(**user)

    # add orders
    orders: dict[dict] = backup.get("orders")
    for order in orders:
        db.add_order(**order)

    return True
