from dataclasses import dataclass
from io import BytesIO

from ..intercontainer_requests import (
    CONTAINER_URLS,
    download_and_delete_order_file,
    order_video_gfx,
    poll_order_status_finished,
)
from ..types.orders import OrderRequestType


@dataclass
class VideoGFXResults:
    success: bool = False
    video: BytesIO | None = None
    error_message: str | None = None


async def process_videogfx(
    quote_text: str | None,
    quote_author: str | None,
    background_file: BytesIO | None,
    foreground_file: BytesIO | None,
    audio_file: BytesIO | None,
    videogfx_type: OrderRequestType = OrderRequestType.VIDEO_AUTO,
    videogfx_container_url: str = CONTAINER_URLS.VideoGfx,
):
    try:
        order_id = order_video_gfx(
            {
                "background_file": background_file,
                "foreground_file": foreground_file if foreground_file else None,
                "audio_file": audio_file if audio_file else None,
                "quote_text": quote_text,
                "quote_author": quote_author,
                "videogfx_type": videogfx_type,
            },
            videogfx_container_url,
        )
        finished_order = poll_order_status_finished(order_id, videogfx_container_url)

        if finished_order["error"]:
            raise Exception(finished_order["error_message"])

        video_filename = finished_order["output_filenames"][0]
        video_file = download_and_delete_order_file(
            video_filename, videogfx_container_url
        )

        return VideoGFXResults(success=True, video=video_file)

    except Exception as e:
        return VideoGFXResults(success=False, error_message=str(e))
