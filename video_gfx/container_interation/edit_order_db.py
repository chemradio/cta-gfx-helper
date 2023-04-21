import requests
from config import EDIT_ORDER_ENDPOINT


def mark_order_video_gfx(order: dict) -> None:
    r = requests.put(
        EDIT_ORDER_ENDPOINT,
        json=order,
    )
    return r.json() if r.status_code == 200 else None
