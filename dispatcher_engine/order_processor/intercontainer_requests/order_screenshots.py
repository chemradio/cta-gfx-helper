import requests

from . import CONTAINER_URLS


def order_screenshots(
    screenshot_url: str,
    container_url: str = CONTAINER_URLS.Screenshoter,
) -> str:
    "return a string containing order id at the slave container"
    r = requests.post(container_url, data={"screenshot_link": screenshot_url})
    return r.json()["order_id"]
