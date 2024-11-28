import asyncio
from io import BytesIO
from uuid import uuid4
from fastapi import APIRouter, File, Form, UploadFile
from db_mongo import Orders
from custom_types_enums import OrderRequestType
from order_processor.order_processor import process_order

router = APIRouter()


@router.post("/")
async def add_new_order(
    request_type: str = Form(...),
    # feedback
    telegram_id: int | None = Form(None),
    email: str | None = Form(None),
    # order meta
    ordered_from: str | None = Form(None),
    created: str | None = Form(None),
    # screenshots
    screenshot_link: str | None = Form(None),
    # quote
    quote_text: str | None = Form(None),
    quote_author_text: str | None = Form(None),
    # readtime
    readtime_text: str | None = Form(None),
    readtime_speed: int | float | None = Form(None),
    # files
    background_file: UploadFile | None = File(None),
    foreground_file: UploadFile | None = File(None),
    audio_file: UploadFile | None = File(None),
):
    order = {
        "id": str(uuid4()),
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

    Orders.insert_one(order)

    asyncio.create_task(process_order(order))
    return Orders.find_one({"id": order["id"]})
