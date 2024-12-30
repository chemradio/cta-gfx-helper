import time
import httpx
import asyncio
from py_gfxhelper_lib.intercontainer_requests import (
    download_and_delete_order_files,
    check_order_status,
)
from pathlib import Path
import secrets
from pprint import pprint

DISPATCHER_URL = "http://127.0.0.1:9000/orders/"


async def add_video_auto_order(order_data: dict) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(DISPATCHER_URL, data=order_data)
        data = response.json()
        return data["order_id"]


async def main():
    orders = [
        add_video_auto_order(
            {
                "request_type": "video_auto",
                "telegram_id": 247066990,
                "email": "chemradio@gmail.com",
                "ordered_from": "telegram",
                "created": str(int(time.time())),
                "screenshot_link": "https://x.com/elonmusk/status/1865457111783637448",
                "quote_text": "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России.",
                "quote_author_text": "Orda.kz",
            }
        ),
        add_video_auto_order(
            {
                "request_type": "video_auto",
                "telegram_id": 247066990,
                "email": "chemradio@gmail.com",
                "ordered_from": "telegram",
                "created": str(int(time.time())),
                "screenshot_link": "https://vk.com/wall141291173_32879",
                "quote_text": "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России.",
                "quote_author_text": "Orda.kz",
            }
        ),
        add_video_auto_order(
            {
                "request_type": "video_auto",
                "telegram_id": 247066990,
                "email": "chemradio@gmail.com",
                "ordered_from": "telegram",
                "created": str(int(time.time())),
                "screenshot_link": "https://www.facebook.com/zuck/posts/10115976683809371?__cft__[0]=AZXUqiHawZL8qgYoSbqfnTBecxJQJMekvot-XIgw9N1KhSqDhytg3gShCOh6T-R46jz_uEk3SRPpmUE647KU3V45ZAq28V27MOMb1jWufB7VrSrVKqWhprVupmYHJ_yX_BIMlJLtBD81tzttxap0tWcZACjNhY-5BM_-Zz7pOUau9CE3AL9dNR6MgoGGRRKpnRU&__tn__=%2CO%2CP-R",
                "quote_text": "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России.",
                "quote_author_text": "Orda.kz",
            }
        ),
        add_video_auto_order(
            {
                "request_type": "video_auto",
                "telegram_id": 247066990,
                "email": "chemradio@gmail.com",
                "ordered_from": "telegram",
                "created": str(int(time.time())),
                "screenshot_link": "https://t.me/durov/342",
                "quote_text": "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России.",
                "quote_author_text": "Orda.kz",
            }
        ),
    ]
    for order in orders:
        order_id = await order
        print(order_id)


if __name__ == "__main__":
    asyncio.run(main())
