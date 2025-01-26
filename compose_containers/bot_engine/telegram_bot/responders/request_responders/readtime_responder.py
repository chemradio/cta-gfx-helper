from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class ReadtimeResponder:
    @staticmethod
    async def ask_readtime_text(user_id):
        return await bot.send_message(
            chat_id=user_id,
            text="📝 Пришли сюда текст.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def bad_text(user_id):
        return await bot.send_message(
            chat_id=user_id,
            text="📝 Это не текст. Скопируй текст в сообщение.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_readtime_speed(user_id):
        readtime_speed_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Медленно", callback_data="slow_readtime"),
                    InlineKeyboardButton(f"Средне", callback_data="medium_readtime"),
                    InlineKeyboardButton(f"Быстро", callback_data="fast_readtime"),
                ]
            ]
        )
        return await bot.send_message(
            chat_id=user_id,
            text="📝 Выбери скорость чтения.",
            reply_markup=readtime_speed_keyboard,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def readtime_results(user_id: int, readtime: str, speed: int):
        results_text = f"📝 Хрон текста: {readtime} \nСкорость {speed} слов в минуту"

        return await bot.send_message(
            chat_id=user_id,
            text=results_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
