import config
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.bot_instance import bot
from telegram import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


class RegisterAdminResponder:
    @staticmethod
    async def register_applied(admin_id, user_id, first_name: str = ""):
        register_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        Responses.register.approve_inline,
                        callback_data=f"approve_{user_id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        Responses.register.block_inline,
                        callback_data=f"block_{user_id}",
                    )
                ],
            ]
        )
        return await bot.send_message(
            chat_id=admin_id,
            text=Responses.register.register_applied_admin.format(
                first_name=first_name, telegram_id=user_id
            ),
            reply_markup=register_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_approved(admin_id, user_id, first_name):
        return await bot.send_message(
            chat_id=admin_id,
            text=Responses.register.register_approved_admin.format(
                first_name=first_name, telegram_id=user_id
            ),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_blocked(admin_id, user_id, first_name):
        return await bot.send_message(
            chat_id=admin_id,
            text=Responses.register.register_blocked_adminformat(
                first_name=first_name, telegram_id=user_id
            ),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
