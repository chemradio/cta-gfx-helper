import interlinks
from engines.telegram_bot.bot_instance import bot
from database.db import db_handler
from telegram import (
    ReplyKeyboardRemove,
    Update,
    ParseMode,
)
from telegram.ext import (
    CallbackContext,
)
from engines.telegram_bot.legacy_handlers.decorators import logger_bot
from engines.telegram_bot.legacy_handlers.question_senders import (
    ask_for_link,
    ask_bg_animation_type,
    ask_for_readtime_text,
)

################################################################
# START and EXIT related funcs
################################################################
def add_start_db_entry(update, status=None):
    logger_bot.debug(
        f"Adding start db entry. First name: {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    db_handler.add_db_entry(
        {
            "status": status,
            "first_name": update.message.from_user.first_name,
            "telegram_id": update.message.from_user.id,
            "chat_id": update.message.chat.id,
            "screenshots_ready": False,
            "video_ready": False,
            "start_timestamp": update.message.date.timestamp(),
            # 'datetime': datetime.datetime.now()
        }
    )


################################################################
def start(update: Update, _: CallbackContext) -> None:
    logger_bot.debug(
        f"Start command. First name: {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    if notify_end_previous_sessions(user_id=update.message.from_user.id, chat_id=update.message.chat.id):
        return

    if db_handler.get_is_user_allowed(user_id=update.message.from_user.id):
        add_start_db_entry(update=update, status="init")
        update.message.reply_text(
            interlinks.stage_texts["common"]["start_message"],
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
        )
        return
    else:
        update.message.reply_text(
            interlinks.stage_texts["unregistered_user"],
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
        )
        return


################################################################
def start_video_auto_production(update: Update, _: CallbackContext) -> None:
    logger_bot.debug(
        f"start_video_auto - First name: {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    if notify_end_previous_sessions(
        user_id=update.message.from_user.id, chat_id=update.message.chat.id
    ):
        return

    if db_handler.get_init_status(user_id=update.message.from_user.id):
        db_handler.activate_init_status(user_id=update.message.from_user.id)
        db_handler.update_db_parameters(
            user_id=update.message.from_user.id,
            parameters={"request_type": "video_auto", "stage": "link"},
        )
        ask_for_link(user_id=update.message.from_user.id)
        return
    else:
        init_failed(update)
        return


################################################################
def start_video_files_production(update: Update, _: CallbackContext) -> None:
    logger_bot.debug(
        f"start_video_files - First name: {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    if notify_end_previous_sessions(
        user_id=update.message.from_user.id, chat_id=update.message.chat.id
    ):
        return

    if db_handler.get_init_status(user_id=update.message.from_user.id):
        db_handler.activate_init_status(user_id=update.message.from_user.id)
        db_handler.update_db_parameters(
            user_id=update.message.from_user.id,
            parameters={"request_type": "video_files", "stage": "bg_animation_type"},
        )
        ask_bg_animation_type(user_id=update.message.from_user.id)
        return
    else:
        init_failed(update)
        return


################################################################
def start_only_screenshots(update: Update, _: CallbackContext) -> None:
    logger_bot.debug(
        f"start_only_screenshots - First name: {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    if notify_end_previous_sessions(
        user_id=update.message.from_user.id, chat_id=update.message.chat.id
    ):
        return

    if db_handler.get_init_status(user_id=update.message.from_user.id):
        db_handler.activate_init_status(user_id=update.message.from_user.id)
        db_handler.update_db_parameters(
            user_id=update.message.from_user.id,
            parameters={"request_type": "only_screenshots", "stage": "link"},
        )
        ask_for_link(user_id=update.message.from_user.id)
        return
    else:
        init_failed(update)
        return


################################################################
def start_readtime(update: Update, _: CallbackContext) -> None:
    logger_bot.debug(
        f"start_readtime - First name: {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    if notify_end_previous_sessions(
        user_id=update.message.from_user.id, chat_id=update.message.chat.id
    ):
        return
    if db_handler.get_init_status(user_id=update.message.from_user.id):
        db_handler.activate_init_status(user_id=update.message.from_user.id)
        db_handler.update_db_parameters(
            user_id=update.message.from_user.id,
            parameters={"request_type": "readtime", "stage": "text"},
        )
        ask_for_readtime_text(user_id=update.message.from_user.id)
        return
    else:
        init_failed(update)
        return


################################################################
def notify_end_previous_sessions(user_id, chat_id):
    logger_bot.debug(f"Check prev sessions - {user_id}")
    if db_handler.get_active_doc_id(user_id):
        bot.send_message(
            chat_id=chat_id,
            text=interlinks.stage_texts["common"]["terminate_sessions_notification"],
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
        )
        return True
    else:
        return False


################################################################
def init_failed(update):
    logger_bot.debug(
        f"INIT failed - {update.message.from_user.first_name} {update.message.from_user.id}"
    )
    bot.send_message(
        chat_id=update.message.chat.id,
        text=interlinks.stage_texts["common"]["start_new_session"],
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.HTML,
    )
    return False
