import requests
from telegram import ReplyKeyboardRemove

import config
from bot_instance import bot


async def report_error(order):
    try:
        await bot.send_message(
            chat_id=order.get("user_telegram_id"),
            text="Произошла ошибка. Перешли это сообщение администатору бота, пожалуйста.\n\n"
            + order.get("error_type"),
            allow_sending_without_reply=True,
            reply_markup=ReplyKeyboardRemove(),
            read_timeout=300,
            write_timeout=300,
            pool_timeout=300,
            connect_timeout=300,
        )
        return True
    except:
        return False


def report_error_raw(order):
    try:
        kwargs = {
            "chat_id": order.get("user_telegram_id"),
            "text": "✅ Твой заказ готов.",
        }

        r = requests.post(
            config.SEND_MESSAGE_TELEGRAM_API_ENDPOINT,
            params=kwargs,
        )
        return True
    except:
        return False
