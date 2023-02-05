import asyncio

from bot_instance import bot
from send_process.report_error import report_error, report_error_raw
from send_process.telegram.send_files import send_files, send_files_raw


async def send_order(order: dict) -> dict:
    if not order.get("error"):
        send_success = await send_files(order)

    else:
        send_success = await report_error(order)

    if send_success:
        order["send_success"] = True
    else:
        order["error"] = "True"
        order["error_type"] = "send_error"

    return order


def send_order_raw(order: dict) -> dict:
    if not order.get("error"):
        send_success = send_files_raw(order)
    else:
        send_success = report_error_raw(order)

    if send_success:
        order["send_success"] = True
    else:
        order["error"] = "True"
        order["error_type"] = "send_error"

    return order
