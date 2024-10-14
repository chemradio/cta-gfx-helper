from dataclasses import dataclass
from io import BytesIO

from ..intercontainer_requests import (
    CONTAINER_URLS,
    delete_order_file,
    download_order_file,
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


def process_screenshots(
    screenshot_url: str, screenshot_container_url: str = CONTAINER_URLS.Screenshoter
) -> ScreenshotResults:
    try:
        order_id = order_screenshots(screenshot_url, screenshot_container_url)
        finished_order = poll_order_status_finished(order_id, screenshot_container_url)

        if finished_order["error"]:
            raise Exception(finished_order["error_message"])

        background_image = download_order_file(
            finished_order["output_filenames"][0], screenshot_container_url
        )
        delete_order_file(
            finished_order["output_filenames"][0], screenshot_container_url
        )

        two_layer = True if len(finished_order["output_filenames"]) > 1 else False
        if two_layer:
            foreground_image = download_order_file(
                finished_order["output_filenames"][1], screenshot_container_url
            )
            delete_order_file(
                finished_order["output_filenames"][1], screenshot_container_url
            )

        return ScreenshotResults(
            success=True,
            background=background_image,
            foreground=foreground_image if two_layer else None,
            two_layer=two_layer,
        )

    except Exception as e:
        return ScreenshotResults(success=False, error_message=str(e))
