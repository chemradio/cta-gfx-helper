from telegram import ForceReply, Update
from telegram.ext import ContextTypes

from container_interaction.helpers import UserStatus
from telegram_bot.callbacks.admin_callbacks.backup_restore_db import (
    backup_db_callback,
    restore_db_callback,
)
from telegram_bot.callbacks.admin_callbacks.list_users_to_admin import (
    list_users_to_admin,
)
from telegram_bot.callbacks.commands.exit_callback import exit_callback
from telegram_bot.callbacks.commands.help_callback import help_callback
from telegram_bot.callbacks.commands.start_callback import start_callback
from telegram_bot.callbacks.register.auth_callback import auth_callback


async def commands_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text:
        command = update.message.text[1:]
    else:
        command = update.message.caption[1:]

    match command:
        case "start":
            return await start_callback(update, context)
        case "exit":
            return await exit_callback(update, context)
        case "help":
            return await help_callback(update, context)
        case "register":
            return await auth_callback(update, context)

        # admin commands
        case "backup":
            return await backup_db_callback(update, context)
        case "restore":
            return await restore_db_callback(update, context)
        case "cookie_file":
            return await ...(update, context)

        case "users_blocked":
            return await list_users_to_admin(UserStatus.BLOCKED)
        case "users_approved":
            return await list_users_to_admin(UserStatus.ALLOWED)
        case "users_pending":
            return await list_users_to_admin(UserStatus.PENDING)
        case "users_all":
            return await list_users_to_admin(UserStatus.ALL)
        case _:
            raise WrongCommand(command=command)


class WrongCommand(Exception):
    def __init__(self, command):
        self.command = command
        super().__init__()

    def __str__(self):
        return f"Wrong command detected: {self.command}"
