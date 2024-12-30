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
        files = dict()

        background_file = order_data.get("background_file")
        if background_file:
            files["background_file"] = (
                "background_file.png",
                order_data.pop("background_file"),
                "image/png",
            )

        foreground_file = order_data.get("foreground_file")
        if foreground_file:
            files["foreground_file"] = (
                "foreground_file.png",
                order_data.pop("foreground_file"),
                "image/png",
            )

        audio_file = order_data.get("audio_file")
        if audio_file:
            files["audio_file"] = (
                "audio_file.wav",
                order_data.pop("audio_file"),
                "audio/wav",
            )
        response = await client.post(DISPATCHER_URL, data=order_data, files=files)
        data = response.json()
        return data


def main():
    asyncio.run(
        add_video_auto_order(
            {
                "request_type": "video_files",
                "telegram_id": 247066990,
                "email": "chemradio@gmail.com",
                "ordered_from": "telegram",
                "created": str(int(time.time())),
                "background_file": open(
                    "/Users/timurtimaev/code/cta-gfx-helper/tests/bg.png", "rb"
                ),
                "foreground_file": open(
                    "/Users/timurtimaev/code/cta-gfx-helper/tests/fg.png", "rb"
                ),
                "quote_text": "По его словам, к расследованию авиакатастрофы привлекли представителей Казахстана, Азербайджана и России.",
                "quote_author_text": "Orda.kz",
            }
        )
    )


if __name__ == "__main__":
    main()
