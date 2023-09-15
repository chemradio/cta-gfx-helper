import json
import os
from pathlib import Path

from db_mongo.db_config.db_init import Users

JSON_PATH = Path.cwd() / "db_mongo" / "seeding" / "optional_seed_data.json"


def seed_users():
    with open(JSON_PATH, "rt") as f:
        data: list[dict] = json.load(f)
        print(f"{data=}")

    for user in data:
        telegram_user = Users.find_one({"telegram_id": user["telegram_id"]})
        if not telegram_user:
            Users.insert_one(user)
