import os

from bson.objectid import ObjectId

from db_mongo.db_config.db_init import Users
from utils.auth.password_hashing import generate_password_hash
from utils.helper_enums.users import NormalUserPermission, UserRole


def seed_admin() -> bool:
    BOT_ADMIN_EMAIL = os.getenv("BOT_ADMIN_EMAIL")
    BOT_ADMIN_PASSWORD = os.getenv("BOT_ADMIN_PASSWORD")
    BOT_ADMIN = int(os.getenv("BOT_ADMIN"))
    update = {
        "role": UserRole.ADMIN,
        "permission": NormalUserPermission.APPROVED,
        "telegram_id": BOT_ADMIN,
        "email": BOT_ADMIN_EMAIL,
        "password_hash": generate_password_hash(BOT_ADMIN_PASSWORD),
    }

    # find user if already exists
    telegram_admin = Users.find_one({"telegram_id": BOT_ADMIN})
    web_admin = Users.find_one({"email": BOT_ADMIN_EMAIL})

    # create new record
    if not telegram_admin and not web_admin:
        Users.insert_one(update)
        return True

    # remove duplicate
    if telegram_admin and web_admin:
        query = {"_id": ObjectId(telegram_admin["_id"])}
        if telegram_admin["_id"] != web_admin["_id"]:
            Users.find_one_and_delete({"_id": ObjectId(web_admin["_id"])})

    elif telegram_admin:
        query = {"_id": ObjectId(telegram_admin["_id"])}
    elif web_admin:
        query = {"_id": ObjectId(web_admin["_id"])}

    else:
        Users.find_one_and_update(
            query,
            {"$set": update},
        )
        return True
