from telegram import ForceReply, Update
from telegram.ext import ContextTypes

from py_gfxhelper_lib.user_enums.user_permission import UserPermission
from py_gfxhelper_lib.user_enums.user_role import UserRole
# from telegram_bot.callbacks.admin_callbacks.backup_restore_db import (
#     backup_db_callback,
#     restore_db_callback,
# )
# from telegram_bot.callbacks.admin_callbacks.cookie_file_uploader import (
#     cookie_file_uploader,
# )
# from telegram_bot.callbacks.commands.admin_command import admin_panel_callback
from telegram_bot.callbacks.commands.back_button import back_callback
from telegram_bot.callbacks.commands.exit_callback import exit_callback
from telegram_bot.callbacks.commands.help_callback import help_callback
from telegram_bot.callbacks.commands.start_callback import start_callback
from telegram_bot.callbacks.register.auth_callback import auth_register_callback


async def commands_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text[1:]

    match command:
        case "start":
            return await start_callback(update, context)
        case "exit":
            return await exit_callback(update, context)
        case "help":
            return await help_callback(update, context)
        case "back":
            return await back_callback(update, context)
        case "register":
            return await auth_register_callback(update, context)

        # admin commands
        # case "backup":
        #     return await backup_db_callback(update, context)
        # case "restore":
        #     return await restore_db_callback(update, context)
        # case "cookie_file":
        #     return await cookie_file_uploader(update, context)

        # case "admin":
        #     return await admin_panel_callback(update, context)
        case _:
            raise Exception(f"Wrong command detected: {command}")


