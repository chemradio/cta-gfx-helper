import httpx
from io import BytesIO
from custom_types import AssetFile


async def convert_file(asset_file: AssetFile) -> AssetFile:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:9005",
            files={"file": (asset_file.random_full_filename, asset_file.bytesio)},
        )

        converted_mime = response.headers["Content-Type"]

        return AssetFile(
            bytes=BytesIO(response.content),
            mime_type=converted_mime,
        )
