from py_gfxhelper_lib.files import AssetFile, FileType
from ..container_processors import process_screenshots


async def process_only_screenshots(order: dict) -> list[AssetFile]:
    output = list()

    screenshots = await process_screenshots(screenshot_url=order["screenshot_link"])
    output.append(
        AssetFile(
            bytes_or_bytesio=screenshots.background.content,
            extension="png",
            file_type=FileType.IMAGE,
        )
    )

    if screenshots.foreground:
        output.append(
            AssetFile(
                bytes_or_bytesio=screenshots.foreground.content,
                extension="png",
                file_type=FileType.IMAGE,
            )
        )

    return output
