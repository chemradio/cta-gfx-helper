from io import BytesIO
from typing import Any

import httpx
from py_gfxhelper_lib.constants import ContainerUrls


# same func just in async with httpx
async def order_video_gfx(
    videogfx_data: dict[str, Any],
    container_url: str = ContainerUrls.VIDEOGFX,
) -> str:
    files = dict()
    background_file: BytesIO = videogfx_data.pop("background_file")
    foreground_file: BytesIO = videogfx_data.pop("foreground_file")
    audio_file: BytesIO = videogfx_data.pop("audio_file")

    if background_file:
        files["background_file"] = ("background_file.png", background_file, "image/png")

    if foreground_file:
        files["foreground_file"] = ("foreground_file.png", foreground_file, "image/png")

    if audio_file:
        files["audio_file"] = ("audio_file.wav", audio_file, "audio/wav")

    async with httpx.AsyncClient() as client:
        r = await client.post(container_url, files=files, data=videogfx_data)
        return r.json()["order_id"]
