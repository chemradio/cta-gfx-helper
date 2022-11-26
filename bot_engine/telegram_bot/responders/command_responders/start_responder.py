import config
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.bot_instance import bot
from telegram import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


class StartResponder:
    @staticmethod
    async def ask_order_type(user_id):
        order_type_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        Responses.request_options.video_auto, callback_data="video_auto"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        Responses.request_options.video_files,
                        callback_data="video_files",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        Responses.request_options.only_screenshots,
                        callback_data="only_screenshots",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        Responses.request_options.readtime, callback_data="readtime"
                    ),
                ],
            ]
        )

        await bot.send_message(
            chat_id=user_id,
            text=Responses.command.start_message,
            reply_markup=order_type_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
