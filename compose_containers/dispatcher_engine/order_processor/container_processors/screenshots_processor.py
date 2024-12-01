from dataclasses import dataclass
from io import BytesIO

from py_gfxhelper_lib.constants import ContainerUrls
from py_gfxhelper_lib.intercontainer_requests import (
    download_and_delete_order_file,
    poll_order_status_finished,
)
from .intercontainer_requests.order_screenshots import order_screenshots


@dataclass
class ScreenshotResults:
    success: bool = False
    background: BytesIO | None = None
    foreground: BytesIO | None = None
    two_layer: bool | None = False
    error_message: str | None = None


async def process_screenshots(
    screenshot_url: str, screenshot_container_url: str = ContainerUrls.SCREENSHOOTER
) -> ScreenshotResults:
    try:
        print(__file__, "ordering screenshots")
        order_id = await order_screenshots(screenshot_url, screenshot_container_url)
        print(__file__, f"{order_id=}")

        print(__file__, "polling order status")
        finished_order = await poll_order_status_finished(
            screenshot_container_url, order_id
        )
        print(__file__, f"{finished_order=}")

        print("downloading files")
        print("downloading and deleting background image")
        background_image = await download_and_delete_order_file(
            screenshot_container_url + "/file_server/",
            finished_order["output_filenames"][0],
        )

        two_layer = True if len(finished_order["output_filenames"]) > 1 else False
        if two_layer:
            foreground_image = await download_and_delete_order_file(
                screenshot_container_url + "/file_server/",
                finished_order["output_filenames"][1],
            )

        return ScreenshotResults(
            success=True,
            background=background_image,
            foreground=foreground_image if two_layer else None,
            two_layer=two_layer,
        )

    except Exception as e:
        return ScreenshotResults(success=False, error_message=str(e))
