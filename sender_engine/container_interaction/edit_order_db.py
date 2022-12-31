import requests

from config import EDIT_ORDER_ENDPOINT


async def mark_order_sent(sent_order) -> None:
    r = requests.post(
        EDIT_ORDER_ENDPOINT,
        json=sent_order,
    )
    return r.json() if r.status_code == 200 else None
