from py_gfxhelper_lib.files import AssetFile, FileType

from .send_functions import send_file_telegram, send_text_telegram


async def return_result_telegram(telegram_id: int, container_output: list[AssetFile]):
    for file_index, result_file in enumerate(container_output):
        match result_file.file_type:
            case FileType.TEXT:
                return await send_text_telegram(
                    text=result_file.text,
                    receiver_id=telegram_id,
                )
            case FileType.VIDEO:
                return await send_file_telegram(
                    filename=result_file.filename,
                    file_bytes=result_file.bytesio,
                    receiver_id=telegram_id,
                )
            case FileType.IMAGE:
                return await send_file_telegram(
                    filename=f"{file_index}_{result_file.filename}",
                    file_bytes=result_file.bytesio,
                    receiver_id=telegram_id,
                )



async def report_error_telegram(telegram_id: int, error_message: str, order: dict):
    return await send_text_telegram(
        text=f"Произошла ошибка при обработке заказа.\n{error_message}\nПожалуйста, перешли это сообщение админу бота\n\n.{order}",
        receiver_id=telegram_id,
    )