import traceback

from py_gfxhelper_lib.order_enums import OrderRequestType, OrderStatus
from db_mongo import Orders
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
        change_db_order_status(order["order_id"], OrderStatus.PROCESSING)
        # general order processing
        # fix quote and audio fields
        order["quote_enabled"] = True if order["quote_text"] else False
        order["audio_enabled"] = True if order["audio_file"] else False

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
        log_db_order_error(order["order_id"], str(e))
        print(f"Error while processing order: {str(e)}", flush=True)
        print(str(e), flush=True)
        traceback.print_exc()

        if order.get("telegram_id"):
            try:
                return await report_error_telegram(
                    telegram_id=order["telegram_id"], error_message=str(e), order=order
                )
            except Exception as e:
                print(str(e))
                pass
    finally:
        change_db_order_status(order["order_id"], OrderStatus.FINISHED)


def change_db_order_status(order_id: str, status: OrderStatus) -> None:
    Orders.find_one_and_update(
        {"order_id": order_id},
        {"$set": {"status": status.value}},
    )


def log_db_order_error(order_id: str, error_message: str) -> None:
    Orders.find_one_and_update(
        {"order_id": order_id},
        {"$set": {"error": True, "error_message": error_message}},
    )
