from typing import Optional

import requests

from config import ORDERS_ENDPOINT


def get_ready_to_video_gfx_order() -> list[dict | None]:
    r = requests.get(ORDERS_ENDPOINT, json={"current_stage": "ready_for_video_gfx"})
    result = r.json()
    return result if result else None
