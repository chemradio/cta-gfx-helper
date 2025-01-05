from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from py_gfxhelper_lib.user_enums.user_permission import UserPermission
from telegram_bot.bot_instance import bot


class RegisterAdminResponder:
    @staticmethod
    async def register_applied(admin_id, user_id, first_name: str = ""):
        register_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Одобрить",
                        callback_data=f"approve_{user_id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ Заблокировать",
                        callback_data=f"block_{user_id}",
                    )
                ],
            ]
        )
        return await bot.send_message(
            chat_id=admin_id,
            text="👤 💡 Новая заявка на регистрацию.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}".format(
                first_name=first_name, telegram_id=user_id
            ),
            reply_markup=register_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_approved(admin_id, user_id, first_name):
        return await bot.send_message(
            chat_id=admin_id,
            text="👤 ✅ Заявка на регистрацию одобрена.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}".format(
                first_name=first_name, telegram_id=user_id
            ),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_blocked(admin_id, user_id, first_name):
        return await bot.send_message(
            chat_id=admin_id,
            text="👤 ❌ Пользователь заблокирован.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}".format(
                first_name=first_name, telegram_id=user_id
            ),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def register_pended(admin_id, user_id, first_name):
        return await bot.send_message(
            chat_id=admin_id,
            text="👤 ❔ Пользователь в ожидании.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}".format(
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
                text = "👤 ✅ Одобренный пользователь.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}".format(
                    first_name=first_name, telegram_id=user_id
                )

            case UserPermission.PENDING:
                text = "👤 ❔ Неодобренный пользователь.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}".format(
                    first_name=first_name, telegram_id=user_id
                )

            case UserPermission.BLOCKED:
                text = "👤 ❌ Заблокированный пользователь.\n\nИмя: {first_name}\nTelegram ID: {telegram_id}".format(
                    first_name=first_name, telegram_id=user_id
                )

            case _:
                text = "unspecified user status type"

        register_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "✅ Одобрить",
                        callback_data=f"approve_{user_id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❌ Заблокировать",
                        callback_data=f"block_{user_id}",
                    )
                ],
                [
                    InlineKeyboardButton(
                        "❔ Решить позже",
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
            text="👤... Пользователи с таким критерием отсутствуют",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
