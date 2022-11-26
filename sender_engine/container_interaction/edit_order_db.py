import requests
from config import EDIT_ORDER_ENDPOINT


def mark_order_sent(order: dict, send_success: bool) -> None:
    r = requests.post(
        EDIT_ORDER_ENDPOINT,
        json={
            "order_id": order["order_id"],
            "status": "success" if send_success else "send_error",
        },
    )
    return r.json() if r.status_code == 200 else None
