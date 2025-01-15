from telegram import Update
from telegram.ext import ContextTypes

import config
from py_gfxhelper_lib.user_enums import UserRole, UserPermission
from container_interaction.users import (
    register_user,
    get_user_role,
    get_user_permission,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import (
    parse_user_first_name,
    parse_user_id,
)
from telegram_bot.responders.main_responder import Responder


async def auth_register_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    user_id = parse_user_id(update)
    first_name = parse_user_first_name(update)

    if user_id == config.BOT_ADMIN:
        return True

    user_role = await get_user_role(user_id)
    if user_role == UserRole.ADMIN:
        return True

    user_permission = await get_user_permission(telegram_id=user_id)

    if user_permission == UserPermission.APPROVED:
        return True

    elif user_permission == UserPermission.BLOCKED:
        print(
            f"Blocked user accessed the bot. First name: {first_name}, Telegram ID: {user_id}"
        )
        return False

    elif user_permission == UserPermission.PENDING:
        await Responder.register_user.register_already_applied(user_id)
        print(
            f"Pending user accessed the bot. First name: {first_name}, Telegram ID: {user_id}"
        )
        return False

    elif user_permission == UserPermission.UNREGISTERED:
        if update.to_dict().get("message", {}).get("text", "") == "/register":
            await register_user(
                telegram_id=user_id, user_data={"first_name": first_name}
            )
            await Responder.register_user.register_applied(user_id)
            await Responder.register_admin.register_applied(
                config.BOT_ADMIN, user_id, first_name=first_name
            )
        else:
            await Responder.register_user.register_not_applied(user_id)
        print(
            f"Unregistered user accessed the bot. First name: {first_name}, Telegram ID: {user_id}"
        )
        return False

    return False
