from io import BytesIO

import httpx


async def download_order_file(filename: str, container_url: str) -> BytesIO:
    async with httpx.AsyncClient() as client:
        r = await client.get(container_url, params={"filename": filename})
        return BytesIO(r.content)


async def delete_order_file(filename: str, container_url: str) -> None:
    async with httpx.AsyncClient() as client:
        r = await client.delete(container_url, params={"filename": filename})
        assert r.status_code == 200


async def download_and_delete_order_file(filename: str, container_url: str) -> BytesIO:
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
