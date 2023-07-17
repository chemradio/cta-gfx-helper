from telegram import Update
from telegram.ext import ContextTypes

import config
from container_interaction.helpers import UserPermission, UserRole
from container_interaction.users_db import (
    add_pending_user,
    check_user_role,
    check_user_status,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import (
    parse_user_first_name,
    parse_user_id,
)
from telegram_bot.callbacks.register.auth_exceptions import (
    BlockedUser,
    PendingUser,
    UnregisteredUser,
)
from telegram_bot.responders.main_responder import Responder


async def auth_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = parse_user_id(update)
    first_name = parse_user_first_name(update)

    user_role = await check_user_role(telegram_id=user_id)
    if user_role == UserRole.ADMIN:
        return True

    user_status = await check_user_status(telegram_id=user_id)

    if user_status == UserPermission.BLOCKED:
        raise BlockedUser(first_name, user_id)

    elif user_status == UserPermission.PENDING:
        await Responder.register_user.register_already_applied(user_id)
        raise PendingUser(first_name, user_id)

    elif user_status == UserPermission.UNREGISTERED:
        if update.message.text == "/register":
            await add_pending_user({"telegram_id": user_id, "first_name": first_name})
            await Responder.register_user.register_applied(user_id)
            await Responder.register_admin.register_applied(
                config.BOT_ADMIN, user_id, first_name=first_name
            )
        else:
            await Responder.register_user.register_not_applied(user_id)
        raise UnregisteredUser(first_name, user_id)
    else:
        return True
