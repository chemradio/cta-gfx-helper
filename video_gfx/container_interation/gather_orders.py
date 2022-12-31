from typing import Optional

import requests

from config import GET_ONE_ORDER_ENDPOINT


def get_ready_to_video_gfx_order() -> Optional[dict]:
    r = requests.get(
        GET_ONE_ORDER_ENDPOINT, json={"current_stage": "ready_for_video_gfx"}
    )
    result = r.json()
    return result if result else None
