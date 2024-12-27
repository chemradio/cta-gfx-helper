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

DISPATCHER_URL = "http://127.0.0.1:9000/orders"


async def add_video_files_order(order_data: dict) -> str:
    async with httpx.AsyncClient() as client:
        files = dict()

        background_file = order_data.pop("background_file")
        if background_file:
            files["background_file"] = (
                "background_file.png",
                background_file,
                "image/png",
            )

        foreground_file = order_data.pop("foreground_file")
        if foreground_file:
            files["foreground_file"] = (
                "foreground_file.png",
                foreground_file,
                "image/png",
            )

        audio_file = order_data.pop("audio_file")
        if audio_file:
            files["audio_file"] = (
                "audio_file.wav",
                audio_file,
                "audio/wav",
            )

        pprint(files)
        pprint(order_data)
        response = await client.post(DISPATCHER_URL, files=files, data=order_data)
        return response.json()["order_id"]


async def process_tests(screenshot_links: list[str]):
    # place orders for each screenshot link
    orders = []
    for screenshot_link in screenshot_links:
        order_id = await add_video_files_order(screenshot_link)
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
    request_type = "video_auto"
    telegram_id = 247066990
    email = "chemradio@gmail.com"
    ordered_from = "telegram"
    created = time.time()

    screenshot_link = None

    quote_text = "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России. Ни одна из этих стран, подчеркнул спикер сената, не заинтересована в том, чтобы скрывать информацию."
    quote_author = "Orda.kz"

    background_file = "/Users/timurtimaev/code/cta-gfx-helper/tests/bg.png"
    foreground_file = "/Users/timurtimaev/code/cta-gfx-helper/tests/fg.png"
    audio_file = ""

    asyncio.run(
        process_tests(
            [
                {
                    "request_type": request_type,
                    "telegram_id": telegram_id,
                    "email": email,
                    "ordered_from": ordered_from,
                    "created": str(created),
                    "screenshot_link": screenshot_link,
                    "quote_text": quote_text,
                    "quote_author_text": quote_author,
                    "background_file": (
                        open(background_file, "rb") if background_file else None
                    ),
                    "foreground_file": (
                        open(foreground_file, "rb") if foreground_file else None
                    ),
                    "audio_file": open(audio_file, "rb") if audio_file else None,
                }
            ],
        )
    )


if __name__ == "__main__":
    main()
