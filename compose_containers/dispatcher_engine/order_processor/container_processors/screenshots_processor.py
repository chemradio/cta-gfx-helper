from dataclasses import dataclass
from io import BytesIO

from .intercontainer_requests import (
    CONTAINER_URLS,
    download_and_delete_order_file,
    order_screenshots,
    poll_order_status_finished,
)


@dataclass
class ScreenshotResults:
    success: bool = False
    background: BytesIO | None = None
    foreground: BytesIO | None = None
    two_layer: bool | None = False
    error_message: str | None = None


async def process_screenshots(
    screenshot_url: str, screenshot_container_url: str = CONTAINER_URLS.Screenshoter
) -> ScreenshotResults:
    try:
        print(__file__, "ordering screenshots")
        order_id = await order_screenshots(screenshot_url, screenshot_container_url)
        print(__file__, f"{order_id=}")

        print(__file__, "polling order status")
        finished_order = await poll_order_status_finished(
            order_id, screenshot_container_url
        )
        print(__file__, f"{finished_order=}")

        print("downloading files")
        print("downloading and deleting background image")
        background_image = await download_and_delete_order_file(
            finished_order["output_filenames"][0],
            screenshot_container_url + "/file_server/",
        )

        two_layer = True if len(finished_order["output_filenames"]) > 1 else False
        if two_layer:
            foreground_image = await download_and_delete_order_file(
                finished_order["output_filenames"][1],
                screenshot_container_url + "/file_server/",
            )

        return ScreenshotResults(
            success=True,
            background=background_image,
            foreground=foreground_image if two_layer else None,
            two_layer=two_layer,
        )

    except Exception as e:
        return ScreenshotResults(success=False, error_message=str(e))
