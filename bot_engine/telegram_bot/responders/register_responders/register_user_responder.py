from telegram import ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot
from telegram_bot.responders.bot_texts import Responses


class RegisterUserResponder:
    @staticmethod
    async def register_not_applied(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.register.register_not_applied,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_applied(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.register.register_applied_user,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_pending(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.register.register_pending_user,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_approved(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.register.register_approved_user,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_already_applied(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.register.register_already_applied,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_already_approved(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.register.register_already_approved,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
