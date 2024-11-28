from custom_types_enums import ContainerOutputFile, FileType
from utils.filenames.filename_generator import FilenameType, generate_filename

from .send_functions import send_file_telegram, send_text_telegram


async def return_result_telegram(
    telegram_id: int, container_output: list[ContainerOutputFile]
):
    # send file to telegram
    for file_index, result_file in enumerate(container_output):
        match result_file.file_type:
            case FileType.TEXT:
                await send_text_telegram(
                    text=result_file.text,
                    receiver_id=telegram_id,
                )
            case FileType.VIDEO:
                await send_file_telegram(
                    filename=generate_filename(FilenameType.VIDEOGFX_VIDEO),
                    file_bytes=result_file.bytes_io,
                    receiver_id=telegram_id,
                )
            case FileType.IMAGE:
                await send_file_telegram(
                    filename=file_index
                    + generate_filename(FilenameType.SCREENSHOT_IMAGE),
                    file_bytes=result_file.bytes_io,
                    receiver_id=telegram_id,
                )
