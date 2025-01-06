from telegram import Update
from telegram.ext import ContextTypes

import config
from telegram_bot.callbacks.admin_callbacks.admin_query_callback import (
    admin_query_callback,
)
from telegram_bot.callbacks.commands.admin_command import admin_panel_callback
from telegram_bot.callbacks.commands.commands_dispatcher import (
    WrongCommand,
    commands_callback,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.callbacks.main_callback.request_callback_router import (
    WrongRequestTypeResponse,
    request_router,
    request_type_callback,
)
from telegram_bot.callbacks.register.auth_callback import auth_callback
from telegram_bot.responders.main_responder import Responder


async def dispatcher_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    # first parse user_id from update.message.from_user.id
    # or update.callback_query.from_user.id
    user_id = parse_user_id(update)

    # if user is admin check if commands, callback_queries contain admin specific elements
    # user approval/blocking, listing orders, etc.
    # if user_id == config.BOT_ADMIN:
    #     try:
    #         admin_actions = await admin_query_callback(update, context)
    #         if admin_actions:
    #             return
    #     except:
    #         pass


    # check user allowance. If user is allowed returns without any issues.
    try:
        await auth_callback(update, context)
    except:
        return

    # collect existing user's current order data
    user_data: dict = context.user_data

    # command handler
    try:
        if update.message.text:
            if update.message.text.startswith("/"):
                return await commands_callback(update, context)

        if update.message.caption:
            if update.message.caption.startswith("/"):
                return await commands_callback(update, context)

    except WrongCommand as e:
        print(e)
        return
    except Exception as e:
        print(e)

    # set request type
    if user_data.get("status") == "init":
        try:
            await request_type_callback(update, context)
        except WrongRequestTypeResponse as e:
            print(str(e))
            return

    # route to appropriate order workflow
    try:
        return await request_router(update, context)
    except:
        user_data.clear()
        return await Responder.errors.no_active_session(user_id)
