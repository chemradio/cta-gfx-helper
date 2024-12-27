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
        pprint(order_data)
        response = await client.post(DISPATCHER_URL, data=order_data)
        return response.json()["order_id"]


async def process_tests(screenshot_links: list[str]):
    # place orders for each screenshot link
    orders = []
    for screenshot_link in screenshot_links:
        order_id = await add_video_auto_order(screenshot_link)
        orders.append(order_id)

    while True:
        tasks = [check_order_status(DISPATCHER_URL, order_id) for order_id in orders]
        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)
            if result.get("status") == "finished":
                files = await download_and_delete_order_files(DISPATCHER_URL, result)
                for file_bytesio in files:
                    with open(
                        f"{result['order_id']}_{secrets.token_hex(8)}.mp4", "wb"
                    ) as f:
                        f.write(file_bytesio.getvalue())
                orders.remove(result["order_id"])
        if not orders:
            break
        await asyncio.sleep(3)


def main():
    asyncio.run(
        process_tests(
            [
                {
                    "request_type": "video_auto",
                    "telegram_id": 247066990,
                    "email": "chemradio@gmail.com",
                    "ordered_from": "telegram",
                    "created": str(int(time.time())),
                    "screenshot_link": "https://meduza.io",
                    "quote_text": "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России.",
                    "quote_author_text": "Orda.kz",
                }
            ],
        )
    )


if __name__ == "__main__":
    main()
