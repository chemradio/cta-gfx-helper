from telegram import ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot
from telegram_bot.responders.bot_texts import Responses


class ErrorsResponder:
    @staticmethod
    async def gp_error(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.error.gp_error,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def no_active_session(user_id):
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.error.no_active_session_notification,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def try_again_error(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.error.try_again_error,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def wrong_audio_format(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.error.wrong_audio_format,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def audio_duration_exceeded(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.error.audio_duration_exceeded,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def max_attachment_size_exceeded(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.error.max_attachment_size_exceeded,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def text_too_short(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.error.text_too_short,
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
