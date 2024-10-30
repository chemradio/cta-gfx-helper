from custom_types.orders import OrderRequestType

from .request_processors import (
    process_only_screenshots,
    process_readtime,
    process_video_auto,
    process_video_files,
    process_video_mixed,
)


async def process_order(order: dict):
    # general order processing
    # fix quote and audio fields
    order.quote_enabled = True if order.quote_text else False
    order.audio_enabled = True if order.audio_file else False

    match order.request_type:
        case OrderRequestType.READTIME:
            return await process_readtime(order)
        case OrderRequestType.ONLY_SCREENSHOTS:
            return await process_only_screenshots(order)
        case OrderRequestType.VIDEO_AUTO:
            return await process_video_auto(order)
        case OrderRequestType.VIDEO_MIXED:
            return await process_video_mixed(order)
        case OrderRequestType.VIDEO_FILES:
            return await process_video_files(order)

    # send file to telegram
