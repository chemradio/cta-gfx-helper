import requests

from config import ORDERS_ENDPOINT


def mark_order_screenshots(order: dict) -> None:
    r = requests.put(
        ORDERS_ENDPOINT,
        json={k: v for k, v in order.items() if v is not None},
    )
    return r.json() if r.status_code == 200 else None
