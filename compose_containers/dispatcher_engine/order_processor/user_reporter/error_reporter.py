from .telegram_reporter.error_report import report_error_telegram


async def report_error_to_user(
    order: dict,
    error_message: str,
):
    if order.get("telegram_id"):
        await report_error_telegram(
            telegram_id=order["telegram_id"], error_message=error_message, order=order
        )


async def report_error_to_admin_telegram(
    order: dict,
    error_message: str,
    admin_telegram_id: int,
):
    await report_error_telegram(
        telegram_id=admin_telegram_id, error_message=error_message, order=order
    )
