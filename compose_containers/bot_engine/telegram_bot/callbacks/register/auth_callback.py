from telegram import Update
from telegram.ext import ContextTypes

import config
from py_gfxhelper_lib.user_enums.user_permission import UserPermission
from py_gfxhelper_lib.user_enums.user_role import UserRole
from container_interaction.users import (
    add_pending_user,
    check_user_role,
    check_user_status,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import (
    parse_user_first_name,
    parse_user_id,
)
from telegram_bot.responders.main_responder import Responder


async def auth_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = parse_user_id(update)
    if user_id == config.BOT_ADMIN:
        return True

    first_name = parse_user_first_name(update)

    user_role = await check_user_role(telegram_id=user_id)
    if user_role == UserRole.ADMIN:
        return True

    user_status = await check_user_status(telegram_id=user_id)

    if user_status == UserPermission.BLOCKED:
        raise Exception(f"Blocked user accessed the bot. First name: {first_name}, Telegram ID: {user_id}")

    elif user_status == UserPermission.PENDING:
        await Responder.register_user.register_already_applied(user_id)
        raise Exception(f"Pending user accessed the bot. First name: {first_name}, Telegram ID: {user_id}")

    elif user_status == UserPermission.UNREGISTERED:
        if update.message.text == "/register":
            await add_pending_user({"telegram_id": user_id, "first_name": first_name})
            await Responder.register_user.register_applied(user_id)
            await Responder.register_admin.register_applied(
                config.BOT_ADMIN, user_id, first_name=first_name
            )
        else:
            await Responder.register_user.register_not_applied(user_id)
        raise Exception(f"Unregistered user accessed the bot. First name: {first_name}, Telegram ID: {user_id}")
    else:
        return True
