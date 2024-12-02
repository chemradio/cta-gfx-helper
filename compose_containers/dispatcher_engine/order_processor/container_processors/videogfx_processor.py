from dataclasses import dataclass
from io import BytesIO


from py_gfxhelper_lib.constants import ContainerUrls
from py_gfxhelper_lib.intercontainer_requests import (
    download_and_delete_order_file,
    poll_order_status_finished,
)
from .intercontainer_requests.order_video_gfx import order_video_gfx
from py_gfxhelper_lib.files import VideoGFXResults


async def process_videogfx(
    quote_text: str | None,
    quote_author: str | None,
    background_file: BytesIO | None,
    foreground_file: BytesIO | None,
    audio_file: BytesIO | None,
    videogfx_container_url: str = ContainerUrls.VIDEOGFX,
) -> VideoGFXResults:
    try:
        order_id = await order_video_gfx(
            {
                "background_file": background_file,
                "foreground_file": foreground_file if foreground_file else None,
                "audio_file": audio_file if audio_file else None,
                "quote_text": quote_text,
                "quote_author": quote_author,
            },
            videogfx_container_url,
        )
        finished_order = await poll_order_status_finished(
            videogfx_container_url, order_id
        )

        if finished_order["error"]:
            raise Exception(finished_order["error_message"])

        video_filename = finished_order["output_filenames"][0]
        video_file = await download_and_delete_order_file(
            videogfx_container_url + "/file_server/", video_filename
        )

        return VideoGFXResults(success=True, video=video_file)

    except Exception as e:
        return VideoGFXResults(success=False, error_message=str(e))
