from telegram import ForceReply, Update
from telegram.ext import ContextTypes
from telegram_bot.callbacks.commands.start_callback import start_callback
from telegram_bot.callbacks.commands.help_callback import help_callback
from telegram_bot.callbacks.commands.exit_callback import exit_callback
from telegram_bot.callbacks.register.auth_callback import auth_callback


async def commands_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    command = update.message.text[1:]
    if command == "start":
        return await start_callback(update, context)
    if command == "exit":
        return await exit_callback(update, context)
    if command == "help":
        return await help_callback(update, context)
    if command == "register":
        return await auth_callback(update, context)
    else:
        raise WrongCommand(command=command)


class WrongCommand(Exception):
    def __init__(self, command):
        self.command = command
        super().__init__()

    def __str__(self):
        return f"Wrong command detected: {self.command}"
