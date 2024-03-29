import requests
from config import ORDERS_ENDPOINT


def get_ready_to_send_order() -> dict | None:
    r = requests.get(
        ORDERS_ENDPOINT,
        json={"current_stage": "ready_for_send", "ordered_from": "telegram"},
    )
    result = r.json()
    return result
