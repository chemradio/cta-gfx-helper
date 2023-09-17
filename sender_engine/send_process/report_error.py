import requests

import config


def report_error_raw(order: dict, user_id: int):
    try:
        kwargs = {
            "chat_id": user_id,
            "text": "Произошла ошибка. Перешли это сообщение администатору бота, пожалуйста.\n\n"
            + order.get("error_type"),
        }

        r = requests.post(
            config.SEND_MESSAGE_TELEGRAM_API_ENDPOINT,
            params=kwargs,
        )
        return True
    except:
        return False

    # @classmethod
    # async def _report_error_to_user(
    #     cls, order: Order, recipient_telegram_id: int
    # ) -> None:
    #     message = f"Произошла ошибка. Пожалуйста, перешли это сообщение администратору.\n\n{dict(order)}"
    #     kwargs = {"chat_id": recipient_telegram_id, "text": message}
    #     r = requests.post(config.TELEGRAM_SEND_MESSAGE_API, params=kwargs)

    # @classmethod
    # async def _send_message(cls, message: str, recipient_telegram_id: int) -> None:
    #     kwargs = {"chat_id": recipient_telegram_id, "text": message}
    #     r = requests.post(config.TELEGRAM_SEND_MESSAGE_API, params=kwargs)
