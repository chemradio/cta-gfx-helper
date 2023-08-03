import requests

from config import VIDEOGFX_ENDPOINT


async def signal_to_video_gfx():
    r = requests.post(VIDEOGFX_ENDPOINT)
    print(r.json())
