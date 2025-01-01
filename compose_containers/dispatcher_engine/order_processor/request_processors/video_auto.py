from py_gfxhelper_lib.files import AssetFile, FileType

from ..container_processors import process_screenshots, process_videogfx


async def process_video_auto(order: dict) -> list[AssetFile]:
    screenshots = await process_screenshots(screenshot_url=order["screenshot_link"])
    videogfx = await process_videogfx(
        quote_text=order["quote_text"],
        quote_author=order["quote_author_text"],
        background_file=screenshots.background.content,
        foreground_file=(
            screenshots.foreground.content if screenshots.foreground else None
        ),
        audio_file=order["audio_file"],
    )

    return [
        AssetFile(
            bytes_or_bytesio=videogfx.video,
            extension="mp4",
            file_type=FileType.VIDEO,
        ),
    ]
