from telegram import Update
from telegram.ext import ContextTypes

import config
from py_gfxhelper_lib.user_enums.user_permission import UserPermission
from py_gfxhelper_lib.user_enums.user_role import UserRole
from container_interaction.users import (
    add_pending_user,
    check_user_role,
    get_user_permission,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import (
    parse_user_first_name,
    parse_user_id,
)
from telegram_bot.responders.main_responder import Responder


async def auth_register_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = parse_user_id(update)
    first_name = parse_user_first_name(update)

    # auto allow admin
    if user_id == config.BOT_ADMIN:
        return True

    # auto allow admin
    user_role = await check_user_role(telegram_id=user_id)
    if user_role == UserRole.ADMIN:
        return True


    user_permission = await get_user_permission(telegram_id=user_id)

    if user_permission == UserPermission.APPROVED:
        return True
    
    elif user_permission == UserPermission.BLOCKED:
        print(f"Blocked user accessed the bot. First name: {first_name}, Telegram ID: {user_id}")
        return False

    elif user_permission == UserPermission.PENDING:
        await Responder.register_user.register_already_applied(user_id)
        print(f"Pending user accessed the bot. First name: {first_name}, Telegram ID: {user_id}")
        return False

    elif user_permission == UserPermission.UNREGISTERED:
        if update.message.text == "/register":
            await add_pending_user({"telegram_id": user_id, "first_name": first_name})
            await Responder.register_user.register_applied(user_id)
            await Responder.register_admin.register_applied(
                config.BOT_ADMIN, user_id, first_name=first_name
            )
        else:
            await Responder.register_user.register_not_applied(user_id)
        print(f"Unregistered user accessed the bot. First name: {first_name}, Telegram ID: {user_id}")
        return False

    return False