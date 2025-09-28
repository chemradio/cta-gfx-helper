from io import BytesIO
from ..files.asset_file import AssetFile
import httpx

import logging

logger = logging.getLogger(__name__)


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
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                file_converter_url,
                files={"file": (asset_file.filename, asset_file.bytesio)},
            )
            response.raise_for_status()

            converted_mime = response.headers["Content-Type"]

            # Handle large responses
            if len(response.content) > 8 * 1024 * 1024:  # 8MB
                # For very large files, consider streaming
                content = BytesIO()
                for chunk in response.iter_bytes():
                    content.write(chunk)
                content.seek(0)
            else:
                content = BytesIO(response.content)

            return AssetFile(
                bytes_or_bytesio=content,
                mime_type=converted_mime,
            )
    except Exception as e:
        logger.error(f"File conversion failed: {str(e)}")
        raise e


async def rescale_image_async(
    asset_file: AssetFile,
    max_width: int | float | None = None,
    max_height: int | float | None = None,
    file_converter_url: str = "http://file_converter:9005",
) -> AssetFile:
    if not max_width and not max_height:
        raise ValueError("At least one of max_width or max_height must be provided")

    dimensions = {}
    if max_width:
        dimensions["max_width"] = max_width
    if max_height:
        dimensions["max_height"] = max_height

    async with httpx.AsyncClient() as client:

        response = await client.post(
            f"{file_converter_url}/rescale_image/",
            files={"original_image": (asset_file.filename, asset_file.bytesio)},
            data=dimensions,
        )
        converted_mime = response.headers["Content-Type"]

        return AssetFile(
            bytes_or_bytesio=BytesIO(response.content),
            mime_type=converted_mime,
        )


def rescale_image_sync(
    asset_file: AssetFile,
    max_width: int | float | None = None,
    max_height: int | float | None = None,
    file_converter_url: str = "http://file_converter:9005",
) -> AssetFile:
    if not max_width and not max_height:
        raise ValueError("At least one of max_width or max_height must be provided")

    dimensions = {}
    if max_width:
        dimensions["max_width"] = max_width
    if max_height:
        dimensions["max_height"] = max_height

    with httpx.Client() as client:
        response = client.post(
            f"{file_converter_url}/rescale_image/",
            files={"original_image": (asset_file.filename, asset_file.bytesio)},
            data=dimensions,
        )
        converted_mime = response.headers["Content-Type"]

        return AssetFile(
            bytes_or_bytesio=BytesIO(response.content),
            mime_type=converted_mime,
        )
