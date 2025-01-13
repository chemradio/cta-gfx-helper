from typing import Any

import httpx
from py_gfxhelper_lib.constants import ContainerUrls
from py_gfxhelper_lib.files.asset_file import AssetFile


async def order_video_gfx(
    videogfx_data: dict[str, Any],
    container_url: str = ContainerUrls.VIDEOGFX,
) -> str:
    files = dict()
    background_file: AssetFile = videogfx_data.pop("background_file", None)
    foreground_file: AssetFile = videogfx_data.pop("foreground_file", None)
    audio_file: AssetFile = videogfx_data.pop("audio_file", None)

    if background_file:
        files["background_file"] = (background_file.filename, background_file.bytesio)

    if foreground_file:
        files["foreground_file"] = (foreground_file.filename, foreground_file.bytesio)

    if audio_file:
        files["audio_file"] = (audio_file.filename, audio_file.bytesio)

    async with httpx.AsyncClient() as client:
        r = await client.post(container_url, files=files, data=videogfx_data)
        return r.json()["order_id"]
