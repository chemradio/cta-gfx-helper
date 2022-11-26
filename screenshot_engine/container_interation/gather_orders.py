import requests
from typing import Optional
from config import LIST_ORDERS_ENDPOINT, GET_ONE_ORDER_ENDPOINT


def get_ready_to_screenshot_orders() -> Optional[list]:
    r = requests.get(LIST_ORDERS_ENDPOINT, json={"status": "screenshots_pending"})
    return r.json()["orders"] if r.status_code == 200 else None


def get_ready_to_screenshot_order() -> dict:
    r = requests.get(GET_ONE_ORDER_ENDPOINT, json={"status": "screenshots_pending"})
    result = r.json()
    return result if result else None
