from custom_types_enums import ContainerOutputFile, FileType

from ..container_processors import process_screenshots, process_videogfx


async def process_video_auto(order: dict) -> list[ContainerOutputFile]:
    print("processing video auto")
    print("ordering screenshots")
    screenshots = await process_screenshots(screenshot_url=order["screenshot_link"])
    print("screenshots completed")
    print(f"{screenshots.success=}")
    print(f"{screenshots.error_message=}")

    print("ordering videogfx")
    videogfx = await process_videogfx(
        quote_text=order["quote_text"],
        quote_author=order["quote_author_text"],
        background_file=screenshots.background,
        foreground_file=screenshots.foreground if screenshots.foreground else None,
        audio_file=order["audio_file"],
    )
    print("videogfx completed")

    return [
        ContainerOutputFile(file_type=FileType.VIDEO, bytes_io=videogfx.video),
    ]
