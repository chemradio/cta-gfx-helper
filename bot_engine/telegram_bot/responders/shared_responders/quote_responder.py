import config
from telegram_bot.responders.bot_texts import Responses
from telegram_bot.bot_instance import bot
from telegram import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


class QuoteResponder:
    @staticmethod
    async def ask_quote_enabled(user_id):
        """Ask user if he needs a QUOTE-BOX."""
        quote_enabled_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Да", callback_data="quote_enabled"),
                    InlineKeyboardButton(f"Нет", callback_data="quote_disabled"),
                ]
            ]
        )

        await bot.send_message(
            chat_id=user_id,
            text=Responses.quote.quote_enabled,
            reply_markup=quote_enabled_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_quote_text(user_id) -> None:
        await bot.send_message(
            chat_id=user_id,
            text=Responses.quote.quote_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_quote_author_enabled(user_id):
        """Ask user if he needs a QUOTE-BOX."""
        quote_author_enabled_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"Да", callback_data="quote_author_enabled"),
                    InlineKeyboardButton(f"Нет", callback_data="quote_author_disabled"),
                ]
            ]
        )

        await bot.send_message(
            chat_id=user_id,
            text=Responses.quote.quote_author_enabled,
            reply_markup=quote_author_enabled_markup,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_quote_author_text(user_id) -> None:
        await bot.send_message(
            chat_id=user_id,
            text=Responses.quote.quote_author_text,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )
