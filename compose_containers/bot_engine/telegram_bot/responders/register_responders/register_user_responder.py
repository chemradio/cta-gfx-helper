from telegram import ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class RegisterUserResponder:
    @staticmethod
    async def register_not_applied(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="👤 💡 Зарегистрируйся - /register",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_applied(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="👤 💡 Твоя заявка на регистрацию принята. Пожалуйста, ожидай.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_pending(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="👤 ⌛ Твоя заявка на регистрацию все еще на рассмотрении.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_approved(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="👤 ✅ Твоя заявка на регистрацию одобрена. Начни новый заказ - /start",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_already_applied(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="👤 💡 Твой запрос еще на рассмотрении. Ожидай.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_already_approved(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="👤 💡 Ты уже зарегистрирован.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
