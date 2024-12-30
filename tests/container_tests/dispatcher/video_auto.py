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
                "request_type": "video_auto",
                "telegram_id": 247066990,
                "email": "chemradio@gmail.com",
                "ordered_from": "telegram",
                "created": str(int(time.time())),
                "screenshot_link": "https://x.com/elonmusk/status/1865457111783637448",
                "quote_text": "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России.",
                "quote_author_text": "Orda.kz",
            }
        )
    )


if __name__ == "__main__":
    main()
