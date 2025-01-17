import traceback
import config
from py_gfxhelper_lib.order_enums import OrderRequestType, OrderStatus
from db_mongo import Orders
from .request_processors import (
    process_only_screenshots,
    process_readtime,
    process_video_auto,
    process_video_files,
    process_video_mixed,
)
from .signals.admin_termination import AdminTerminatedException
from .user_reporter import (
    return_order_result_to_user,
    report_error_to_user,
    report_error_to_admin,
)


async def process_order(order: dict) -> None:
    try:
        error_message = None
        change_db_order_status(order["order_id"], OrderStatus.PROCESSING)

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

        await return_order_result_to_user(order, container_output)

    except AdminTerminatedException as e:
        error_message = str(e)
        print(f"Admin terminated order: {str(e)}", flush=True)
        await report_error_to_user(order, str(e))
        await report_error_to_admin(order, str(e), config.BOT_ADMIN)

    except Exception as e:
        error_message = str(e)
        print(f"Error while processing order: {str(e)}", flush=True)
        traceback.print_exc()
        await report_error_to_user(order, str(e))
        await report_error_to_admin(order, str(e), config.BOT_ADMIN)

    finally:
        if error_message:
            log_db_order_error(order["order_id"], error_message)
        change_db_order_status(order["order_id"], OrderStatus.FINISHED)
        return None


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
