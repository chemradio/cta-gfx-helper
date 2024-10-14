import requests

from config import SENDER_ENDPOINT


async def signal_to_sender():
    r = requests.post(SENDER_ENDPOINT)
    print(r.json())
