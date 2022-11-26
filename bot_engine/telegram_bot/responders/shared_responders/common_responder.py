import config
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.bot_instance import bot
from telegram import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


class CommonResponder:
    @staticmethod
    async def sessions_terminated_start(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.common.sessions_terminated_start,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def terminate_sessions_notification(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.common.terminate_sessions_notification,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def start_new_session(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.common.start_new_session,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def wait_for_gfx(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.common.wait_for_gfx,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def wait_for_processing(user_id) -> None:
        return await bot.send_message(
            chat_id=user_id,
            text=Responses.common.wait_for_processing,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
