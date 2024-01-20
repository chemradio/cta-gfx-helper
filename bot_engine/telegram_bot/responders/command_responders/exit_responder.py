from telegram import ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class ExitResponder:
    @staticmethod
    async def exit_terminate_order(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="❎ Текущий заказ отменен. Начать новый - /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    async def exit_missing_order(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="❎ У тебя нет незавершенных заказов. Начать новый - /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
