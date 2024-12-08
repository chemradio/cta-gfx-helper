from io import BytesIO
from ..files.asset_file import AssetFile
import httpx


async def download_and_delete_order_files(
    container_url: str, order: dict
) -> list[BytesIO]:
    order_filenames = order.get("output_filenames")
    if not order_filenames:
        return []

    output = []
    for filename in order_filenames:
        file = await download_and_delete_container_file(container_url, filename)
        output.append(file)

    return output


async def download_container_file(base_container_url: str, filename: str) -> BytesIO:
    async with httpx.AsyncClient() as client:
        print(f"Downloading file: {filename}")
        print(f"Base container url: {base_container_url}")
        r = await client.get(
            base_container_url + "/file_server", params={"filename": filename}
        )
        print(r.status_code)

        return BytesIO(r.content)


async def delete_container_file(container_url: str, filename: str) -> None:
    async with httpx.AsyncClient() as client:
        r = await client.delete(container_url, params={"filename": filename})
        assert r.status_code == 200


async def download_and_delete_container_file(
    base_container_url: str, filename: str
) -> BytesIO:
    download_tries = 3
    error_message = ""
    while download_tries > 0:
        try:
            file = await download_container_file(base_container_url, filename)
            await delete_container_file(filename, base_container_url)
            return file
        except Exception as e:
            print(f"Failed to download file: {e}")
            download_tries -= 1
    else:
        print(f"Failed to download file: {error_message}")
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
