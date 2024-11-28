from pprint import pprint

from custom_types_enums.orders import OrderRequestType

from .request_processors import (
    process_only_screenshots,
    process_readtime,
    process_video_auto,
    process_video_files,
    process_video_mixed,
)
from .telegram_send import return_result_telegram


async def process_order(order: dict) -> None:
    try:
        print("received order", flush=True)
        # pprint(order, flush=True)

        # general order processing
        # fix quote and audio fields
        order["quote_enabled"] = True if order["quote_text"] else False
        order["audio_enabled"] = True if order["audio_file"] else False

        print(
            "order request type matching processing", order["request_type"], flush=True
        )
        match order["request_type"]:
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

        print("finished processing, sending to telegram", flush=True)
        if order["telegram_id"]:
            await return_result_telegram(
                telegram_id=order["telegram_id"],
                container_output=container_output,
            )
            print("sent to telegram", flush=True)
    except Exception as e:
        print(f"Error while processing order: {e}")
        print(str(e))
        pprint(order)
        # send error message to telegram
