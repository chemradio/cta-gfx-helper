from telegram import ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class CommonResponder:
    @staticmethod
    async def sessions_terminated_start(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text="❎ Все предыдущие заказы отменены. Новый заказ - /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def terminate_sessions_notification(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text="❌ Пожалуйста, отмени предыдущий незавершенный заказ командой /exit",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def start_new_session(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text="💡 Новый заказ - /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def wait_for_gfx(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text="⏳ Пожалуйста, подожди. Скоро твоя видео-графика будет готова.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def wait_for_processing(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text="⏳ Заказ все еще обрабатывается. Пожалуйста, подожди.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def wait_for_download(user_id):
        return await bot.send_message(
            chat_id=user_id,
            text="⏳ Скачиваю файл...",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
