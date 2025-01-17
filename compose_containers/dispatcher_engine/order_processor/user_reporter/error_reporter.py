from .telegram_reporter import report_error_telegram


async def report_error_to_user(order: dict, error_message: str) -> bool:
    if order.get("telegram_id"):
        await report_error_telegram(
            telegram_id=order["telegram_id"], error_message=error_message, order=order
        )
        return True

    return False


async def report_error_to_admin(
    order: dict, error_message: str, admin_telegram_id: int
) -> bool:
    await report_error_telegram(
        telegram_id=admin_telegram_id, error_message=error_message, order=order
    )
    return True
