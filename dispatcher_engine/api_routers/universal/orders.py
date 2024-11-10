import asyncio
from io import BytesIO
from typing import Optional

from fastapi import APIRouter, File, Form, UploadFile

from custom_types_enums import OrderRequestType
from order_processor.order_processor import process_order

router = APIRouter()


@router.post("/")
async def add_new_order(
    # feedback
    telegram_id: Optional[int] = Form(None),
    email: Optional[str] = Form(None),
    # order meta
    request_type: str = Form(...),
    ordered_from: Optional[str] = Form(None),
    created: Optional[str] = Form(None),
    # screenshots
    screenshot_link: Optional[str] = Form(None),
    # quote
    quote_text: Optional[str] = Form(None),
    quote_author_text: Optional[str] = Form(None),
    # readtime
    readtime_text: Optional[str] = Form(None),
    readtime_speed: Optional[int | float] = Form(None),
    # files
    background_file: Optional[UploadFile] = File(None),
    foreground_file: Optional[UploadFile] = File(None),
    audio_file: Optional[UploadFile] = File(None),
):
    order = {
        "telegram_id": telegram_id,
        "email": email,
        "request_type": OrderRequestType(request_type),
        "ordered_from": ordered_from,
        "created": created,
        "screenshot_link": screenshot_link,
        "quote_text": quote_text,
        "quote_author_text": quote_author_text,
        "readtime_text": readtime_text,
        "readtime_speed": readtime_speed,
        "background_file": (
            BytesIO(background_file.file.read()) if background_file else None
        ),
        "foreground_file": (
            BytesIO(foreground_file.file.read()) if foreground_file else None
        ),
        "audio_file": BytesIO(audio_file.file.read()) if audio_file else None,
    }

    # # save order in db
    # order_db_id = Orders.insert_one(order).inserted_id
    # order = Orders.find_one({"_id": ObjectId(order_db_id)})
    # print(order.dict())

    asyncio.create_task(process_order(order))
    return order
