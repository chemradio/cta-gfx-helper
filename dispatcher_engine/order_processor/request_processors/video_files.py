from custom_types import ContainerOutputFile, FileType

from ..container_processors import process_videogfx


async def process_video_files(order: dict) -> list[ContainerOutputFile]:
    videogfx = await process_videogfx(
        quote_text=order["quote_text"],
        quote_author=order["quote_author_text"],
        background_file=order["background_file"],
        foreground_file=order["foreground_file"] if order["foreground_file"] else None,
        audio_file=order["audio_file"],
    )

    return [
        ContainerOutputFile(file_type=FileType.VIDEO, bytes_io=videogfx.video),
    ]
