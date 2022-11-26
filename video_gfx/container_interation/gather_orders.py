import requests
from typing import Optional
from config import GET_ONE_ORDER_ENDPOINT


def get_ready_to_video_gfx_order() -> Optional[dict]:
    r = requests.get(GET_ONE_ORDER_ENDPOINT, json={"status": "video_gfx_pending"})
    result = r.json()
    return result if result else None
