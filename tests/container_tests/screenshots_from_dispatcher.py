from py_gfxhelper_lib.constants import ContainerUrls
from py_gfxhelper_lib.intercontainer_requests import (
    download_and_delete_order_files,
    poll_order_status_finished,
    check_order_status,
)
from py_gfxhelper_lib.custom_types import Screenshot, ScreenshotResults, ScreenshotRole
import httpx

from py_gfxhelper_lib.constants import ContainerUrls


async def order_screenshots(
    screenshot_url: str,
    container_url: str = "http://127.0.0.1:9002",
) -> str:
    async with httpx.AsyncClient() as client:
        print(
            f"Sending screenshot order to container={container_url}, screenshot_url={screenshot_url}",
            flush=True,
        )
        r = await client.post(container_url, data={"screenshot_link": screenshot_url})
        return r.json()["order_id"]


async def process_screenshots(
    screenshot_url: str, screenshot_container_url: str = "http://127.0.0.1:9002"
) -> ScreenshotResults:
    try:
        order_id = await order_screenshots(screenshot_url, screenshot_container_url)

        finished_order = await poll_order_status_finished(
            screenshot_container_url, order_id
        )
        files = await download_and_delete_order_files(
            screenshot_container_url, finished_order
        )

        two_layer = True if len(finished_order["output_filenames"]) > 1 else False

        if two_layer:
            background_image, foreground_image = files
        else:
            background_image = files[0]

        return ScreenshotResults(
            success=True,
            background=Screenshot(
                content=background_image,
                role=ScreenshotRole.FULL_SIZE,
            ),
            foreground=(
                Screenshot(
                    content=foreground_image,
                    role=ScreenshotRole.POST,
                )
                if two_layer
                else None
            ),
            two_layer=two_layer,
        )

    except Exception as e:
        return ScreenshotResults(success=False, error_message=str(e))


import asyncio

asyncio.run(process_screenshots("https://meduza.io"))
