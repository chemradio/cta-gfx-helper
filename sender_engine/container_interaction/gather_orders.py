import requests
from typing import Optional
from config import GET_ONE_ORDER_ENDPOINT


def get_ready_to_send_order() -> Optional[list]:
    r = requests.get(GET_ONE_ORDER_ENDPOINT, json={"status": "ready_to_send"})
    result = r.json()
    return result if result else None
