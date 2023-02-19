import json
import os
import time
from datetime import datetime, timedelta
from pprint import pprint

from fastapi import APIRouter, BackgroundTasks, Form, HTTPException, Request, UploadFile

from api_routers.signal_sender import signal_to_services
from db.sql_handler import db
from processors.cleanup_order_assets import cleanup_order_assets
from processors.orders import advance_order_stage
from processors.save_user_file_to_volume import save_user_file_to_volume
from processors.token_manupulation import decode_jwt_payload, generate_jwt_token
from processors.vitaly_converters import vitaly_order_converter, vitaly_user_converter

router = APIRouter()

# # orders
# @router.post("/add_order_telegram")
# def add_order(order: dict, background_tasks: BackgroundTasks):
#     order["ordered_from"] = "telegram"
#     order = advance_order_stage(order)
#     db.add_order(**order)
#     background_tasks.add_task(signal_to_services, order.get("current_stage"))
#     return True


@router.post("/add_order_web")
async def add_order_web(
    request: Request,
    background_tasks: BackgroundTasks,
    status: str = Form(None),
    request_type: str = Form(None),
    stage: str = Form(None),
    # link
    link: str = Form(None),
    # quote
    quote_enabled: bool = Form(False),
    quote_text: str = Form(None),
    quote_author_text: str = Form(None),
    # audio
    audio_enabled: bool = Form(False),
    # audio_name: UploadFile | None = None,
    audio_name: str = Form(None),
    # custom layers
    # fore_ground: UploadFile | None = None,
    # back_ground: UploadFile | None = None,
    fore_ground: str = Form(None),
    back_ground: str = Form(None),
):
    # decode_cookie
    jwt_cookie = request.cookies.get("jwt")
    print(jwt_cookie)
    if jwt_cookie:
        try:
            user_data = decode_jwt_payload(jwt_cookie)
        except:
            raise HTTPException(400, detail="Cookie verification failed")
    else:
        raise HTTPException(401, detail="Unauthorized")

    # form_dict = dict(await request.form())
    form_dict = {
        "status": status,
        "request_type": request_type,
        "stage": stage,
        "link": link,
        "quote_enabled": quote_enabled,
        "quote_text": quote_text,
        "quote_author_text": quote_author_text,
        "audio_enabled": audio_enabled,
        "ordered_from": "web"
        # "audio_name": audio_name,
        # "fore_ground": fore_ground,
        # "back_ground": back_ground,
    }

    # handle file saves
    pass

    form_dict["user_email"] = user_data["email"]
    order_dict = vitaly_order_converter(form_dict)
    order = advance_order_stage(order_dict)
    order = db.add_order(**order_dict)
    pprint(order)
    # background_tasks.add_task(signal_to_services, order.get("current_stage"))
    return order


@router.get("/")
def get_active_orders():
    """Returns all active orders from user in a form of a list."""

    return [
        {
            "order_id": 1,
            "request_type": "video_auto",
            "status": "ready",
            "download_links": ["https://fakelink/link1.mp4"],
            "error_message": None,
            "expiry": int((datetime.now() + timedelta(hours=8)).timestamp()),
        },
        {
            "order_id": 2,
            "request_type": "video_files",
            "status": "processing",
            "download_links": [],
            "error_message": None,
            "expiry": int((datetime.now() + timedelta(hours=12)).timestamp()),
        },
        {
            "order_id": 3,
            "request_type": "video_files",
            "status": "error",
            "error_message": "Произошла ошибка захвата скриншотов",
            "download_links": [],
            "expiry": int((datetime.now() + timedelta(hours=24)).timestamp()),
        },
    ]

    current_stage = request.get("current_stage")

    request_status = request.get("status")
    status = request_status if request_status else "active"

    order = db.get_one_order(current_stage, status)
    if not order:
        return None

    # generate and cleanup the order dict
    order_dict = order.__dict__
    order_dict.pop("_sa_instance_state")
    print("get_one_log")
    print(f"{order_dict=}")
    updated_order = advance_order_stage(order_dict)
    print(f"{updated_order=}")
    db.edit_order(**updated_order)
    return order
