from py_gfxhelper_lib.files import AssetFile, FileType

from .send_functions import send_file_telegram, send_text_telegram


async def return_result_telegram(telegram_id: int, container_output: list[AssetFile]):
    for file_index, result_file in enumerate(container_output):
        match result_file.file_type:
            case FileType.TEXT:
                await send_text_telegram(
                    text=result_file.text,
                    receiver_id=telegram_id,
                )
            case FileType.VIDEO:
                await send_file_telegram(
                    filename=result_file.filename,
                    file_bytes=result_file.bytesio,
                    receiver_id=telegram_id,
                )
            case FileType.IMAGE:
                await send_file_telegram(
                    filename=f"{file_index}_{result_file.filename}",
                    file_bytes=result_file.bytesio,
                    receiver_id=telegram_id,
                )
