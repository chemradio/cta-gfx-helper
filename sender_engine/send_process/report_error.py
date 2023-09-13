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
