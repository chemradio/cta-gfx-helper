from container_interaction.get_user_db import get_one_user
from send_process.report_error import report_error_raw
from send_process.telegram.send_files import send_files_raw


def send_order_raw(order: dict) -> dict:
    user = get_one_user(order["user_id"])

    if not order.get("error"):
        send_success = send_files_raw(order, user["telegram_id"])
    else:
        send_success = report_error_raw(order, user["telegram_id"])

    if send_success:
        order["send_success"] = True
    else:
        order["error"] = "True"
        order["error_type"] = "send_error"

    return order
