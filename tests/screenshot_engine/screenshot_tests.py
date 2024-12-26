import json
import httpx
import asyncio
from py_gfxhelper_lib.intercontainer_requests import (
    download_and_delete_order_files,
    check_order_status,
)
from pathlib import Path
import secrets

SCREENSHOOTER_URL = "http://127.0.0.1:9002"


async def add_screenshot_order(screenshot_link: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            SCREENSHOOTER_URL, data={"screenshot_link": screenshot_link}
        )
        return response.json()["order_id"]


async def process_tests(screenshot_links: list[str]):
    # place orders for each screenshot link
    orders = []
    for screenshot_link in screenshot_links:
        order_id = await add_screenshot_order(screenshot_link)
        orders.append(order_id)

    while True:
        tasks = [check_order_status(SCREENSHOOTER_URL, order_id) for order_id in orders]
        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)
            if result.get("status") == "finished":
                files = await download_and_delete_order_files(SCREENSHOOTER_URL, result)
                for file_bytesio in files:
                    with open(
                        f"{result['order_id']}_{secrets.token_hex(8)}.png", "wb"
                    ) as f:
                        f.write(file_bytesio.getvalue())
                orders.remove(result["order_id"])
        if not orders:
            break
        await asyncio.sleep(3)


def main():
    with open(Path(__file__).parent / "screenshot_links.json", "r") as f:
        screenshot_links = json.load(f)

    asyncio.run(
        process_tests(
            [
                "https://www.facebook.com/zuck/posts/10115976683809371?__cft__[0]=AZXUqiHawZL8qgYoSbqfnTBecxJQJMekvot-XIgw9N1KhSqDhytg3gShCOh6T-R46jz_uEk3SRPpmUE647KU3V45ZAq28V27MOMb1jWufB7VrSrVKqWhprVupmYHJ_yX_BIMlJLtBD81tzttxap0tWcZACjNhY-5BM_-Zz7pOUau9CE3AL9dNR6MgoGGRRKpnRU&__tn__=%2CO%2CP-R",
                "https://vk.com/wall141291173_32879",
                "https://t.me/durov/342",
                "https://x.com/elonmusk/status/1865457111783637448",
            ]
            # screenshot_links.get("singleLayer"),
        )
    )


if __name__ == "__main__":
    main()
