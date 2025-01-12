from pprint import pprint

from custom_types_enums.orders import OrderRequestType

from .request_processors import (
    process_only_screenshots,
    process_readtime,
    process_video_auto,
    process_video_files,
    process_video_mixed,
)
from .telegram_send import return_result_telegram, report_error_telegram


async def process_order(order: dict) -> None:
    try:
        # general order processing
        # fix quote and audio fields
        order["quote_enabled"] = True if order["quote_text"] else False
        order["audio_enabled"] = True if order["audio_file"] else False

        from pprint import pprint
        pprint(order)
        print(order,flush=True)
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

        if order.get("telegram_id"):
            return await return_result_telegram(
                telegram_id=order["telegram_id"],
                container_output=container_output,
            )
    except Exception as e:
        print(f"Error while processing order: {str(e)}", flush=True)
        print(str(e), flush=True)
        pprint(order)
        if order.get("telegram_id"):
            try:
                return await report_error_telegram(telegram_id=order["telegram_id"],error_message=str(e), order=order)
            except Exception as e:
                print(str(e))
                pass
