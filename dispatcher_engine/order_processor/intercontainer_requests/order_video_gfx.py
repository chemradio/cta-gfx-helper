import requests

from . import CONTAINER_URLS


def order_video_gfx(
    videogfx_data: dict,
    container_url: str = CONTAINER_URLS.VideoGfx,
) -> str:
    "return a string containing order id at the slave container"
    r = requests.post(container_url, data=videogfx_data)
    return r.json()["order_id"]
