from fastapi import APIRouter
from db.sql_handler import db
import config
import json

router = APIRouter()


@router.post("/cookie_file")
async def add_cookie_file(cookie_file: dict):
    """add a cookie file for browser authentication in screenshots module"""
    with open(config.COOKIE_FILE_PATH, "w+") as cookie_fp:
        json.dump(cookie_file, cookie_fp)
    return True
