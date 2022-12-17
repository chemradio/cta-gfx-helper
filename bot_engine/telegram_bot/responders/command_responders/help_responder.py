from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot
from telegram_bot.responders.bot_texts import Responses


class HelpResponder:
    @staticmethod
    async def help(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.command.help_message,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )