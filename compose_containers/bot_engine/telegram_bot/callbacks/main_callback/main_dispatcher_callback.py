from telegram import Update
from telegram.ext import ContextTypes

import config
from telegram_bot.callbacks.admin_callbacks.admin_query_callback import (
    admin_query_callback,
)
from telegram_bot.callbacks.commands.admin_command import admin_panel_callback
from telegram_bot.callbacks.commands.commands_dispatcher import (
    commands_callback,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.callbacks.main_callback.request_callback_router import (
    request_router,
    request_type_callback,
)
from telegram_bot.callbacks.register.auth_callback import auth_register_callback
from telegram_bot.responders.main_responder import Responder


async def dispatcher_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = parse_user_id(update)

    # check user allowance and or handle register and auth
    user_allowed = await auth_register_callback(update, context)
    if not user_allowed:
        return

    # if user is admin check if commands, callback_queries contain admin specific elements
    # user approval/blocking, listing orders, etc.
    # if user_id == config.BOT_ADMIN:
    #     try:
    #         admin_actions = await admin_query_callback(update, context)
    #         if admin_actions:
    #             return
    #     except:
    #         pass

    user_data: dict = context.user_data
    update_dict = update.to_dict()
    update_message_text = update_dict.get("message", {}).get("text", "")
    order_status = user_data.get("status")

    if update_message_text.startswith("/"):
        return await commands_callback(update, context)

    try:
        if order_status == "init":
            try:
                await request_type_callback(update, context)
            except Exception as e:
                print(str(e))
                return

        # route to appropriate order workflow
        try:
            return await request_router(update, context)
        except:
            user_data.clear()
            await Responder.errors.no_active_session(user_id)
            return

    except Exception as e:
        print(str(e))
        await Responder.errors.custom_error(user_id=user_id, error_text=str(e))
        return await Responder.errors.gp_error(user_id)
