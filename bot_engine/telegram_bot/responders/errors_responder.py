from telegram import ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class ErrorsResponder:
    @staticmethod
    async def gp_error(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🆘 Что-то пошло не так. Попробуй снова или начни сначала - /exit",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def no_active_session(user_id):
        return await bot.send_message(
            chat_id=user_id,
            text="💡 Сначала нажми /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def try_again_error(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🆘 Что-то пошло не так. Попробуй снова.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def wrong_audio_format(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🆘🔊 Этот аудио-файл не поддерживается. Или это вовсе не аудио. Попробуй другой файл.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def audio_duration_exceeded(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🆘🔊 Этот аудио-файл длиннее 40 секунд. Попробуй другой.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def max_attachment_size_exceeded(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🆘🔊 Слишком большой файл. Не могу скачать.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def text_too_short(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="🆘 Текст слишком короткий.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def custom_error(user_id, error_text: str):
        await bot.send_message(
            chat_id=user_id,
            text=error_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
