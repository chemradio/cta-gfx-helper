from typing import Any, Callable

from telegram import Update
from telegram.ext import ContextTypes

import config
from container_interaction.helpers import UserStatus
from container_interaction.users_db import add_pending_user, check_user_status
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.callbacks.register.auth_exceptions import (
    BlockedUser,
    PendingUser,
    UnregisteredUser,
)
from telegram_bot.responders.main_responder import Responder


async def auth_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print("entered auth_callback")
    user_id = parse_user_id(update)
    first_name = update.message.from_user.first_name

    user_status = await check_user_status(telegram_id=user_id)

    if user_status == UserStatus.BLOCKED:
        raise BlockedUser(first_name, user_id)

    elif user_status == UserStatus.PENDING:
        await Responder.register_user.register_already_applied(user_id)
        raise PendingUser(first_name, user_id)

    elif user_status == UserStatus.UNREGISTERED:
        if update.message.text == "/register":
            await add_pending_user({"telegram_id": user_id, "first_name": first_name})
            await Responder.register_user.register_applied(user_id)
            await Responder.register_admin.register_applied(config.BOT_ADMIN, user_id)
        else:
            await Responder.register_user.register_not_applied(user_id)
        raise UnregisteredUser(first_name, user_id)
    else:
        return True
