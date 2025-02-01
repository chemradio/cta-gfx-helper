from .send_functions import send_text_telegram


async def report_error_telegram(telegram_id: int, error_message: str, order: dict):
    return await send_text_telegram(
        text=f"Произошла ошибка при обработке заказа.\n{error_message}\nПожалуйста, перешли это сообщение админу бота.\n\n{str(order)}",
        receiver_id=telegram_id,
    )
