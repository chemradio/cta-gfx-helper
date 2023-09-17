import requests

from config import ORDERS_ENDPOINT


def get_ready_to_screenshot_order() -> list[dict]:
    r = requests.get(ORDERS_ENDPOINT, json={"current_stage": "ready_for_screenshots"})
    result = r.json()
    print(f"Gathered orders: {result}, {type(result)}", flush=True)
    return result if result else None
