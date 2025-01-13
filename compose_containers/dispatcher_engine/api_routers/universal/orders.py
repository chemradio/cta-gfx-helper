import asyncio
from io import BytesIO
from uuid import uuid4
from fastapi import APIRouter, File, Form, UploadFile
from db_mongo import Orders
from custom_types_enums import OrderRequestType
from order_processor.order_processor import process_order
from py_gfxhelper_lib.files.asset_file import AssetFile
router = APIRouter()


@router.post("/", response_model=dict)
async def add_new_order(
    request_type: str = Form(None),
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
        "order_id": str(uuid4()),
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
            AssetFile(bytes_or_bytesio=background_file.file.read(), extension=background_file.filename.split(".")[-1])
        ) if background_file else None,
        "foreground_file": (
            AssetFile(bytes_or_bytesio=foreground_file.file.read(), extension=background_file.filename.split(".")[-1])
        ) if foreground_file else None,
        "audio_file": (
            AssetFile(bytes_or_bytesio=audio_file.file.read(), extension=audio_file.filename.split(".")[-1])
        ) if audio_file else None,
    }

    Orders.insert_one(
        {
            k: "BytesIO placeholder" if isinstance(v, AssetFile) else v
            for k, v in order.items()
        }
    )

    asyncio.create_task(process_order(order))
    
    order = Orders.find_one({"order_id": order["order_id"]})
    order.pop("_id")
    return order
