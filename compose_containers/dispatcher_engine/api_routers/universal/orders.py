import asyncio
import time
from uuid import uuid4
import pymongo
from fastapi import APIRouter, File, Form, UploadFile
from db_mongo import Orders
from py_gfxhelper_lib.order_enums import OrderRequestType, OrderStatus, OrderSource
from order_processor.order_processor import process_order
from py_gfxhelper_lib.files.asset_file import AssetFile

router = APIRouter()


@router.post("/", response_model=dict)
async def add_new_order(
    request_type: OrderRequestType = Form(),
    # feedback
    telegram_id: int | None = Form(None),
    email: str | None = Form(None),
    # order meta
    ordered_from: OrderSource = Form(),
    created: int | None = Form(None),
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
        "request_type": request_type.value,
        "ordered_from": ordered_from,
        "created": created if created else int(time.time()),
        "screenshot_link": screenshot_link,
        "quote_text": quote_text,
        "quote_author_text": quote_author_text,
        "readtime_text": readtime_text,
        "readtime_speed": readtime_speed,
        "background_file": (
            (
                AssetFile(
                    bytes_or_bytesio=background_file.file.read(),
                    extension=background_file.filename.split(".")[-1],
                )
            )
            if background_file
            else None
        ),
        "foreground_file": (
            (
                AssetFile(
                    bytes_or_bytesio=foreground_file.file.read(),
                    extension=background_file.filename.split(".")[-1],
                )
            )
            if foreground_file
            else None
        ),
        "audio_file": (
            (
                AssetFile(
                    bytes_or_bytesio=audio_file.file.read(),
                    extension=audio_file.filename.split(".")[-1],
                )
            )
            if audio_file
            else None
        ),
        "status": OrderStatus.NEW.value,
        "error": False,
    }

    Orders.insert_one(
        {
            k: "AssetFile placeholder" if isinstance(v, AssetFile) else v
            for k, v in order.items()
        }
    )

    asyncio.create_task(process_order(order))

    order = Orders.find_one({"order_id": order["order_id"]})
    order.pop("_id")
    return order


@router.get("/list/")
async def get_orders(
    telegram_id: int | None = None,
    email: str | None = None,
    status: OrderStatus | None = None,
    ordered_from: OrderSource | None = None,
):
    params = {
        "telegram_id": telegram_id,
        "email": email,
        "status": status.value if status else None,
        "ordered_from": ordered_from.value if ordered_from else None,
    }
    filtered_params = {k: v for k, v in params.items() if v is not None}
    orders = Orders.find(filtered_params)
    if not orders:
        return []
    return [
        {k: v for k, v in order.items() if k != "_id"}
        for order in orders.sort("created", pymongo.DESCENDING)
    ]
