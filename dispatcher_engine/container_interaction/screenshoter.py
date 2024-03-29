import requests

from config import SCREENSHOTER_ENDPOINT


async def signal_to_screenshoter(order: dict = {}):
    r = requests.post(SCREENSHOTER_ENDPOINT, json=order)
    print(r.json())
