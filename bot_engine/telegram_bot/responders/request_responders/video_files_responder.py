import inspect

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

import config
from telegram_bot.bot_instance import bot
from telegram_bot.responders.bot_texts import Responses


class VideoFilesResponder:
    @staticmethod
    async def ask_main_file(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.video_files.send_main_file,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_background_source(user_id):
        bg_source_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"Zoom", callback_data="background_screenshot"
                    ),
                    InlineKeyboardButton(f"Scroll", callback_data="background_file"),
                    InlineKeyboardButton(f"Zoom", callback_data="no_background"),
                ]
            ]
        )

        await bot.send_message(
            chat_id=user_id,
            text=Responses.video_files.select_background_source,
            reply_markup=bg_source_keyboard,
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_background_file(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.video_files.send_background_file,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )

    @staticmethod
    async def ask_background_link(user_id):
        await bot.send_message(
            chat_id=user_id,
            text=Responses.video_files.send_background_link,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
        )


class VideoFilesResponderLegacy:
    ...
    # @staticmethod
    # async def ask_bg_file(user_id):
    #     await bot.send_message(
    #         chat_id=user_id,
    #         text=Responses.video_files.seng_bg,
    #         reply_markup=ReplyKeyboardRemove(),
    #         parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
    #     )

    # @staticmethod
    # async def ask_bg_animation(user_id):
    #     bg_type_keyboard = InlineKeyboardMarkup(
    #         [
    #             [
    #                 InlineKeyboardButton(f"Scroll", callback_data="bg_scroll"),
    #                 InlineKeyboardButton(f"Zoom", callback_data="bg_zoom"),
    #             ]
    #         ]
    #     )

    #     await bot.send_message(
    #         chat_id=user_id,
    #         text=Responses.video_files.bg_animation_type,
    #         reply_markup=bg_type_keyboard,
    #         parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
    #     )

    # @staticmethod
    # async def ask_fg_enabled(user_id):
    #     fg_enabled_keyboard = InlineKeyboardMarkup(
    #         [
    #             [
    #                 InlineKeyboardButton(f"Да", callback_data="fg_enabled"),
    #                 InlineKeyboardButton(f"Нет", callback_data="fg_disabled"),
    #             ]
    #         ]
    #     )

    #     await bot.send_message(
    #         chat_id=user_id,
    #         text=Responses.video_files.fg_enabled,
    #         reply_markup=fg_enabled_keyboard,
    #         parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
    #     )

    # @staticmethod
    # async def ask_fg_file(user_id):
    #     await bot.send_message(
    #         chat_id=user_id,
    #         text=Responses.video_files.seng_fg,
    #         reply_markup=ReplyKeyboardRemove(),
    #         parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
    #     )

    # @staticmethod
    # async def ask_fg_animation(user_id):
    #     fg_type_keyboard = InlineKeyboardMarkup(
    #         [
    #             [
    #                 InlineKeyboardButton(f"Scroll", callback_data="fg_scroll"),
    #                 InlineKeyboardButton(f"Zoom", callback_data="fg_zoom"),
    #             ]
    #         ]
    #     )

    #     await bot.send_message(
    #         chat_id=user_id,
    #         text=Responses.video_files.fg_animation_type,
    #         reply_markup=fg_type_keyboard,
    #         parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
    #     )

    # @staticmethod
    # async def results(user_id, context: ContextTypes.DEFAULT_TYPE):
    #     results = inspect.cleandoc(
    #         f"""\
    #         Заказ на графику из файлов

    #         Анимация заднего плана:
    #         {context.user_data.get('bg_type')}

    #         Анимация переднего плана:
    #         {context.user_data.get('fg_type', 'Отсутствует')}

    #         Текст цитаты:
    #         {context.user_data.get('quote_text', 'Отсутствует')}

    #         Автор цитаты:
    #         {context.user_data.get('quote_author_text', 'Отсутствует')}

    #         Аудио:
    #         {context.user_data.get('audio_enabled', 'Отсутствует')}
    #     """
    #     )

    #     results_correct_keyboard = InlineKeyboardMarkup(
    #         [
    #             [
    #                 InlineKeyboardButton(f"Все верно", callback_data="results_correct"),
    #                 InlineKeyboardButton(
    #                     f"Отменить заказ", callback_data="results_incorrect"
    #                 ),
    #             ]
    #         ]
    #     )

    #     await bot.send_message(
    #         chat_id=user_id,
    #         text=results,
    #         reply_markup=results_correct_keyboard,
    #         parse_mode=config.GLOBAL_MESSAGE_PARSE_MODE,
    #     )
