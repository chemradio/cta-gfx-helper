from py_gfxhelper_lib.files import AssetFile, FileType

from ..container_processors import process_videogfx


async def process_video_files(order: dict) -> list[AssetFile]:
    videogfx = await process_videogfx(
        quote_text=order["quote_text"],
        quote_author_text=order["quote_author_text"],
        background_file=order["background_file"],
        foreground_file=order["foreground_file"] if order["foreground_file"] else None,
        audio_file=order["audio_file"],
    )

    return [
        AssetFile(
            bytes_or_bytesio=videogfx.video,
            extension="mp4",
            file_type=FileType.VIDEO,
        ),
    ]
