from interlinks import stage_texts
from engines.telegram_bot import bot

from telegram import (
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
)

from engines.telegram_bot import bot
from handlers.decorators import log_decorator

@log_decorator
def ask_for_link(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["common"]["link"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_bg_animation_type(user_id):
    bg_animation_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Scroll", callback_data="bg_animation_scroll"),
                InlineKeyboardButton(f"Zoom", callback_data="bg_animation_zoom"),
            ]
        ]
    )
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["video_files"]["bg_animation_type"],
        reply_markup=bg_animation_markup,
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_send_bg(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["video_files"]["seng_bg"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_fg_enabled(user_id):
    fg_enabled_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Да", callback_data="fg_enabled"),
                InlineKeyboardButton(f"Нет", callback_data="fg_disabled"),
            ]
        ]
    )
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["video_files"]["fg_enabled"],
        reply_markup=fg_enabled_keyboard,
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_send_fg(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["video_files"]["seng_fg"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_fg_animation_type(user_id):
    fg_animation_type_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"Facebook", callback_data="fg_animation_facebook"
                ),
                InlineKeyboardButton(
                    f"Instagram", callback_data="fg_animation_instagram"
                ),
                InlineKeyboardButton(
                    f"Document", callback_data="fg_animation_document"
                ),
            ]
        ]
    )
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["video_files"]["fg_animation_type"],
        reply_markup=fg_animation_type_keyboard,
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_round_corners_enabled(user_id):
    round_corners_enabled_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Да", callback_data="round_corners_enabled"),
                InlineKeyboardButton(f"Нет", callback_data="round_corners_disabled"),
            ]
        ]
    )
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["video_files"]["round_corners_enabled"],
        reply_markup=round_corners_enabled_keyboard,
        parse_mode=ParseMode.HTML,
    )


#### QUOTE-BOX ####
################################################################
@log_decorator
def ask_quote_enabled(user_id):
    """Ask user if he needs a QUOTE-BOX."""
    quote_enabled_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Да", callback_data="quote_enabled"),
                InlineKeyboardButton(f"Нет", callback_data="quote_disabled"),
            ]
        ]
    )
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["quote"]["quote_enabled"],
        reply_markup=quote_enabled_markup,
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_quote_text(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["quote"]["quote_text"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_quote_author_enabled(user_id):
    """Ask user if he needs a QUOTE-BOX author specified."""
    quote_author_enabled_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Да", callback_data="quote_author_enabled"),
                InlineKeyboardButton(f"Нет", callback_data="quote_author_disabled"),
            ]
        ]
    )
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["quote"]["quote_author_enabled"],
        reply_markup=quote_author_enabled_markup,
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_quote_author_text(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["quote"]["quote_author_text"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_audio_enabled(user_id):
    audio_enabled_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Да", callback_data="audio_enabled"),
                InlineKeyboardButton(f"Нет", callback_data="audio_disabled"),
            ]
        ]
    )
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["audio"]["audio_enabled"],
        reply_markup=audio_enabled_markup,
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_send_audio(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["audio"]["send_audio"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_for_readtime_text(user_id):
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["readtime"]["send_text"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )


################################################################
@log_decorator
def ask_readtime_speed(user_id):
    readtime_speed_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(f"Медленно", callback_data="slow_readtime"),
                InlineKeyboardButton(f"Средне", callback_data="medium_readtime"),
                InlineKeyboardButton(f"Быстро", callback_data="fast_readtime"),
            ]
        ]
    )
    bot.send_message(
        chat_id=user_id,
        text=stage_texts["readtime"]["set_speed"],
        reply_markup=readtime_speed_keyboard,
        parse_mode=ParseMode.HTML,
    )