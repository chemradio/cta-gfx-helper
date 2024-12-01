from io import BytesIO
from ..files.asset_file import AssetFile
import httpx


async def download_order_file(container_url: str, filename: str) -> BytesIO:
    async with httpx.AsyncClient() as client:
        r = await client.get(container_url, params={"filename": filename})
        return BytesIO(r.content)


async def delete_order_file(container_url: str, filename: str) -> None:
    async with httpx.AsyncClient() as client:
        r = await client.delete(container_url, params={"filename": filename})
        assert r.status_code == 200


async def download_and_delete_order_file(container_url: str, filename: str) -> BytesIO:
    download_tries = 3
    while download_tries > 0:
        try:
            file = await download_order_file(filename, container_url)
            await delete_order_file(filename, container_url)
            return file
        except Exception:
            download_tries -= 1
    else:
        raise Exception("Failed to download file. Deletion aborted.")


async def convert_file(asset_file: AssetFile) -> AssetFile:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:9005",
            files={"file": (asset_file.filename, asset_file.bytesio)},
        )

        converted_mime = response.headers["Content-Type"]

        return AssetFile(
            bytes=BytesIO(response.content),
            mime_type=converted_mime,
        )
