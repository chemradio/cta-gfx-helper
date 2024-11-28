import requests
from config import ORDERS_ENDPOINT


def mark_order_video_gfx(order: dict) -> None:
    r = requests.put(
        ORDERS_ENDPOINT,
        json=order,
    )
    return r.json() if r.status_code == 200 else None
