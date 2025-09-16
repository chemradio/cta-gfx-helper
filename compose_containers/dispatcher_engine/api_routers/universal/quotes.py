import asyncio
import time
import pymongo
from fastapi import APIRouter, Form
from db_mongo import Quotes

from py_gfxhelper_lib.order_enums import QuoteApproveStatus
from order_processor.order_processor import process_order
from py_gfxhelper_lib.files.asset_file import AssetFile

router = APIRouter()


@router.post("/", response_model=dict)
async def add_edit_quote(
    telegram_order_id: str = Form(),
    quote_text: str | None = Form(None),
    quote_author_text: str | None = Form(None),
    quote_approve_status: QuoteApproveStatus = Form(QuoteApproveStatus.PENDING),
):
    quote = {
        k: v
        for k, v in {
            "created": int(time.time()),
            "telegram_order_id": telegram_order_id,
            "quote_text": quote_text,
            "quote_author_text": quote_author_text,
            "quote_approve_status": quote_approve_status.value,
        }.items()
        if v is not None
    }

    existing_quote = Quotes.find_one({"telegram_order_id": telegram_order_id})
    if existing_quote:
        Quotes.update_one({"telegram_order_id": telegram_order_id}, {"$set": quote})
    else:
        Quotes.insert_one(quote)

    return {"status": "success", "quote": quote}
