from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from container_interaction.helpers import UserPermission
from telegram_bot.bot_instance import bot
from telegram_bot.responders.bot_texts import Responses


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
            text=Responses.register.register_blocked_admin.format(
                first_name=first_name, telegram_id=user_id
            ),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_pended(admin_id, user_id, first_name):
        return await bot.send_message(
            chat_id=admin_id,
            text=Responses.register.register_pended_admin.format(
                first_name=first_name, telegram_id=user_id
            ),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    #################################
    # /users comand for admin lists users in different categoried
    # following responders are for allowing / blocking / pending existing users

    @staticmethod
    async def list_user(admin_id, user_status: UserPermission, user_id, first_name):
        match user_status:
            case UserPermission.APPROVED:
                text = Responses.register.list_approved_user.format(
                    first_name=first_name, telegram_id=user_id
                )

            case UserPermission.PENDING:
                text = Responses.register.list_pending_user.format(
                    first_name=first_name, telegram_id=user_id
                )

            case UserPermission.BLOCKED:
                text = Responses.register.list_blocked_user.format(
                    first_name=first_name, telegram_id=user_id
                )

            case _:
                text = "unspecified user status type"

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
                [
                    InlineKeyboardButton(
                        Responses.register.pend_inline,
                        callback_data=f"pend_{user_id}",
                    )
                ],
            ]
        )

        return await bot.send_message(
            chat_id=admin_id,
            text=text,
            reply_markup=register_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def empty_users_list(admin_id):
        return await bot.send_message(
            chat_id=admin_id,
            text=Responses.register.empty_users_list,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
