from custom_types import ContainerOutputFile, FileType

from ..container_processors import process_screenshots


async def process_only_screenshots(order: dict) -> list[ContainerOutputFile]:
    output = list()

    screenshots = await process_screenshots(screenshot_url=order["link"])
    output.append(
        ContainerOutputFile(file_type=FileType.IMAGE, bytes_io=screenshots.background)
    )

    if screenshots.foreground:
        output.append(
            ContainerOutputFile(
                file_type=FileType.IMAGE, bytes_io=screenshots.foreground
            )
        )

    return output
