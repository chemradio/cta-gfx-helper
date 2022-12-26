from typing import Optional

import requests

from config import GET_ONE_ORDER_ENDPOINT


def get_ready_to_send_order() -> Optional[list]:
    try:
        r = requests.get(GET_ONE_ORDER_ENDPOINT, json={"current_stage": "ready_to_send"})
        result = r.json()
        return result
    except:
        return None
