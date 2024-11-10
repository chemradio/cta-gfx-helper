from custom_types_enums import ContainerOutputFile, FileType

from ..container_processors import process_screenshots, process_videogfx


async def process_video_mixed(order: dict) -> list[ContainerOutputFile]:
    screenshots = await process_screenshots(screenshot_url=order["link"])
    videogfx = await process_videogfx(
        quote_text=order["quote_text"],
        quote_author=order["quote_author_text"],
        background_file=screenshots.background,
        foreground_file=order["foreground_file"],
        audio_file=order["audio_file"],
    )
    return [
        ContainerOutputFile(file_type=FileType.VIDEO, bytes_io=videogfx.video),
    ]
