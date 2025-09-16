import httpx
from pprint import pprint
from py_gfxhelper_lib.order_enums import OrderSource, OrderStatus, QuoteApproveStatus


QUOTE_ENDPOINT = "http://dispatcher:9003/quotes/"


async def edit_approve_quote(
    telegram_order_id: int,
    quote_approve_status: QuoteApproveStatus = QuoteApproveStatus.PENDING,
    quote_text: str | None = None,
    quote_author_text: str | None = None,
) -> None:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            QUOTE_ENDPOINT,
            data={
                k: v
                for k, v in {
                    "telegram_order_id": telegram_order_id,
                    "quote_approve_status": quote_approve_status.value,
                    "quote_text": quote_text,
                    "quote_author_text": quote_author_text,
                }.items()
                if v is not None
            },
        )
        return r.json()
