from io import BytesIO
from ..files.asset_file import AssetFile
import httpx


async def download_and_delete_order_files(
    base_container_url: str, order: dict
) -> list[BytesIO]:
    order_filenames = order.get("output_filenames")
    if not order_filenames:
        return []

    output = []
    for filename in order_filenames:
        download_tries = 3
        error_message = ""

        while download_tries > 0:
            try:
                file = await download_container_file(base_container_url, filename)
                await delete_container_file(base_container_url, filename)
                output.append(file)
                break
            except Exception as e:
                error_message = str(e)
                download_tries -= 1
        else:
            raise Exception(f"Failed to download file: {filename} - {error_message}")

    return output


async def download_container_file(base_container_url: str, filename: str) -> BytesIO:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            base_container_url + "/file_server", params={"filename": filename}
        )
        return BytesIO(r.content)


async def delete_container_file(container_url: str, filename: str) -> None:
    async with httpx.AsyncClient() as client:
        r = await client.delete(
            container_url + "/file_server", params={"filename": filename}
        )
        assert r.status_code == 200


async def convert_file(
    asset_file: AssetFile, file_converter_url: str = "http://file_converter:9005"
) -> AssetFile:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            file_converter_url,
            files={"file": (asset_file.filename, asset_file.bytesio)},
        )

        converted_mime = response.headers["Content-Type"]

        return AssetFile(
            bytes_or_bytesio=BytesIO(response.content),
            mime_type=converted_mime,
        )


async def rescale_image(
    asset_file: AssetFile,
    max_width: int | float | None = None,
    max_height: int | float | None = None,
    file_converter_url: str = "http://file_converter:9005",
) -> AssetFile:
    async with httpx.AsyncClient() as client:

        response = await client.post(
            f"{file_converter_url}/rescale_image/",
            files={"original_image": (asset_file.filename, asset_file.bytesio)},
            data={
                "max_width": int(max_width) if max_width else None,
                "max_height": int(max_height) if max_height else None,
            },
        )
        converted_mime = response.headers["Content-Type"]

        return AssetFile(
            bytes_or_bytesio=BytesIO(response.content),
            mime_type=converted_mime,
        )
