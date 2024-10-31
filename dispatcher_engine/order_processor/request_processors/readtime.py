from custom_types import ContainerOutputFile, FileType


async def process_readtime(order: dict) -> list[ContainerOutputFile]:

    ...

    return [
        ContainerOutputFile(file_type=FileType.TEXT, text=""),
    ]
