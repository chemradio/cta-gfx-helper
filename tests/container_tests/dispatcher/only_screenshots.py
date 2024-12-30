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


def main():
    asyncio.run(
        add_video_auto_order(
            {
                "request_type": "only_screenshots",
                "telegram_id": 247066990,
                "email": "chemradio@gmail.com",
                "ordered_from": "telegram",
                "created": str(int(time.time())),
                "screenshot_link": "https://www.facebook.com/zuck/posts/10115976683809371?__cft__[0]=AZXUqiHawZL8qgYoSbqfnTBecxJQJMekvot-XIgw9N1KhSqDhytg3gShCOh6T-R46jz_uEk3SRPpmUE647KU3V45ZAq28V27MOMb1jWufB7VrSrVKqWhprVupmYHJ_yX_BIMlJLtBD81tzttxap0tWcZACjNhY-5BM_-Zz7pOUau9CE3AL9dNR6MgoGGRRKpnRU&__tn__=%2CO%2CP-R",
            }
        )
    )


if __name__ == "__main__":
    main()
