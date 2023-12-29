from telegram import ReplyKeyboardRemove

import config
from telegram_bot.bot_instance import bot


class HelpResponder:
    @staticmethod
    async def help(user_id):
        await bot.send_message(
            chat_id=user_id,
            text="💡 ...",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
