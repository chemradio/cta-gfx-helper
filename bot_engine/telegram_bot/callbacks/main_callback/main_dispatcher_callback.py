import config
from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.callbacks.admin_callback.admin_callback import admin_callback
from telegram_bot.callbacks.register.auth_callback import auth_callback
from telegram_bot.responders.main_responder import Responder
from telegram_bot.callbacks.commands.commands_dispatcher import (
    commands_callback,
    WrongCommand,
)
from telegram_bot.callbacks.main_callback.main_callback_helpers import (
    parse_user_id,
)
from telegram_bot.callbacks.main_callback.request_callback_router import (
    request_type_callback,
    WrongRequestTypeResponse,
    request_router,
)


async def dispatcher_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:

    # first parse user_id from update.message.from_user.id
    # or update.callback_query.from_user.id
    user_id = parse_user_id(update)

    # # if user is admin check if commands, callback_queries contain admin specific elements
    # # user approval/blocking, listing orders, etc.
    # if user_id == config.BOT_ADMIN:
    #     try:
    #         await admin_callback(update, context)
    #     except:
    #         pass

    # # check user allowance. If user is allowed returns without any issues.
    # try:
    #     await auth_callback(update, context)
    # except:
    #     return

    # collect existing user's current order data
    user_data: dict = context.user_data

    # command handler
    try:
        if update.message.text.startswith("/"):
            return await commands_callback(update, context)
    except WrongCommand as e:
        print(e)
        return
    except:
        print("Not a command")

    # set request type
    if user_data.get("status") == "init":
        try:
            await request_type_callback(update, context)
        except WrongRequestTypeResponse as e:
            print(e)
            return

    # route to appropriate order workflow
    try:
        return await request_router(update, context)
    except:
        user_data.clear()
        return await Responder.errors.no_active_session(user_id)
