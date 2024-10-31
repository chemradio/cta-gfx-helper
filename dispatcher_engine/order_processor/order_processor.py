from custom_types import FileType
from custom_types.orders import OrderRequestType
from utils.filenames.filename_generator import FilenameType, generate_filename

from .request_processors import (
    process_only_screenshots,
    process_readtime,
    process_video_auto,
    process_video_files,
    process_video_mixed,
)
from .telegram_send.telegram_send import send_file_telegram, send_text_telegram


async def process_order(order: dict) -> None:
    # general order processing
    # fix quote and audio fields
    order["quote_enabled"] = True if order["quote_text"] else False
    order["audio_enabled"] = True if order["audio_file"] else False

    match order.request_type:
        case OrderRequestType.READTIME:
            container_output = await process_readtime(order)
        case OrderRequestType.ONLY_SCREENSHOTS:
            container_output = await process_only_screenshots(order)
        case OrderRequestType.VIDEO_AUTO:
            container_output = await process_video_auto(order)
        case OrderRequestType.VIDEO_MIXED:
            container_output = await process_video_mixed(order)
        case OrderRequestType.VIDEO_FILES:
            container_output = await process_video_files(order)

    # send file to telegram
    for file_index, result_file in enumerate(container_output):
        match result_file.file_type:
            case FileType.TEXT:
                await send_text_telegram(
                    text=result_file.text,
                    receiver_id=order["telegram_id"],
                )
            case FileType.VIDEO:
                await send_file_telegram(
                    filename=generate_filename(FilenameType.VIDEOGFX_VIDEO),
                    file_bytes=result_file.bytes_io,
                    receiver_id=order["telegram_id"],
                )
            case FileType.IMAGE:
                await send_file_telegram(
                    filename=file_index
                    + generate_filename(FilenameType.SCREENSHOT_IMAGE),
                    file_bytes=result_file.bytes_io,
                    receiver_id=order["telegram_id"],
                )
