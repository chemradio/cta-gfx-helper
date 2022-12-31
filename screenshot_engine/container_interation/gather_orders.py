from typing import Optional

import requests

from config import GET_ONE_ORDER_ENDPOINT, LIST_ORDERS_ENDPOINT


def get_ready_to_screenshot_order() -> dict:
    r = requests.get(
        GET_ONE_ORDER_ENDPOINT, json={"current_stage": "ready_for_screenshots"}
    )
    result = r.json()
    return result if result else None
