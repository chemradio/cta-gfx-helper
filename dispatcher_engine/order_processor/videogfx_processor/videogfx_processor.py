from dataclasses import dataclass
from io import BytesIO

from ..intercontainer_requests import (
    CONTAINER_URLS,
    delete_order_file,
    download_order_file,
    order_video_gfx,
    poll_order_status_finished,
)
from ..screenshots_processor.screenshots_processor import process_screenshots
from ..types.videogfx_types import VideoGFXType


@dataclass
class VideoGFXResults:
    success: bool = False
    video: BytesIO | None = None
    error_message: str | None = None


def process_videogfx(
    screenshot_url: str | None,
    quote_text: str | None,
    quote_author: str | None,
    audio_file: BytesIO | None,
    videogfx_type: VideoGFXType = VideoGFXType.AUTO,
    screenshot_container_url: str = CONTAINER_URLS.Screenshoter,
    videogfx_container_url: str = CONTAINER_URLS.VideoGfx,
):
    try:
        screenshot_results = process_screenshots(
            screenshot_url, screenshot_container_url
        )

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

        return VideoGFXResults(success=True, video=...)

    except Exception as e:
        return VideoGFXResults(success=False, error_message=str(e))
