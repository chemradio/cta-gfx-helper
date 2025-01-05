import httpx
import asyncio
from py_gfxhelper_lib.intercontainer_requests import (
    download_and_delete_order_files,
    check_order_status,
)
import secrets

VIDEOGFX_URL = "http://127.0.0.1:9004"


async def add_videogfx_order(gfx_data: dict) -> str:
    async with httpx.AsyncClient() as client:
        files = dict()

        background_file = gfx_data.pop("background_file")
        if background_file:
            files["background_file"] = (
                "background_file.png",
                background_file,
                "image/png",
            )

        foreground_file = gfx_data.pop("foreground_file")
        if foreground_file:
            files["foreground_file"] = (
                "foreground_file.png",
                foreground_file,
                "image/png",
            )

        audio_file = gfx_data.pop("audio_file")
        if audio_file:
            files["audio_file"] = (
                "audio_file.wav",
                audio_file,
                "audio/wav",
            )

        print(files)
        print(gfx_data)
        response = await client.post(VIDEOGFX_URL, files=files, data=gfx_data)
        return response.json()["order_id"]


async def process_tests(screenshot_links: list[str]):
    # place orders for each screenshot link
    orders = []
    for screenshot_link in screenshot_links:
        order_id = await add_videogfx_order(screenshot_link)
        orders.append(order_id)

    while True:
        tasks = [check_order_status(VIDEOGFX_URL, order_id) for order_id in orders]
        results = await asyncio.gather(*tasks)
        for result in results:
            print(result)
            if result.get("status") == "finished":
                files = await download_and_delete_order_files(VIDEOGFX_URL, result)
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
    background_file = "/Users/timurtimaev/code/cta-gfx-helper/tests/bg.png"
    foreground_file = "/Users/timurtimaev/code/cta-gfx-helper/tests/fg.png"
    audio_file = ""
    quote_text = "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России. Ни одна из этих стран, подчеркнул спикер сената, не заинтересована в том, чтобы скрывать информацию."
    quote_author = "Orda.kz"

    asyncio.run(
        process_tests(
            [
                {
                    "background_file": (
                        open(background_file, "rb") if background_file else None
                    ),
                    "foreground_file": (
                        open(foreground_file, "rb") if foreground_file else None
                    ),
                    "audio_file": open(audio_file, "rb") if audio_file else None,
                    "quote_text": quote_text,
                    "quote_author_text": quote_author,
                },
                {
                    "background_file": (
                        open(background_file, "rb") if background_file else None
                    ),
                    "foreground_file": (
                        open(foreground_file, "rb") if foreground_file else None
                    ),
                    "audio_file": open(audio_file, "rb") if audio_file else None,
                    "quote_text": quote_text,
                    "quote_author_text": quote_author,
                },
                {
                    "background_file": (
                        open(background_file, "rb") if background_file else None
                    ),
                    "foreground_file": (
                        open(foreground_file, "rb") if foreground_file else None
                    ),
                    "audio_file": open(audio_file, "rb") if audio_file else None,
                    "quote_text": quote_text,
                    "quote_author_text": quote_author,
                },
                {
                    "background_file": (
                        open(background_file, "rb") if background_file else None
                    ),
                    "foreground_file": (
                        open(foreground_file, "rb") if foreground_file else None
                    ),
                    "audio_file": open(audio_file, "rb") if audio_file else None,
                    "quote_text": quote_text,
                    "quote_author_text": quote_author,
                },
            ],
        )
    )


if __name__ == "__main__":
    main()
