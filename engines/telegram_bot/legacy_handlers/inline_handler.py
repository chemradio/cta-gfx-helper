import time
import interlinks
from engines.telegram_bot.bot_instance import bot
from engines.utils import calc_readtime
from database.db import db_handler
from telegram import (
    ReplyKeyboardRemove,
    Update,
    ParseMode,
)
from telegram.ext import (
    CallbackContext,
)

from engines.telegram_bot.legacy_handlers.error_responses import (
    no_active_session_notification,
)

from engines.telegram_bot.legacy_handlers.check_results import (
    check_results,
)
from engines.telegram_bot.legacy_handlers.process_order import process_order

from engines.telegram_bot.legacy_handlers.question_senders import (
    ask_quote_text,
    ask_audio_enabled,
    ask_quote_author_text,
    ask_send_bg,
    ask_send_fg,
    ask_quote_enabled,
    ask_round_corners_enabled,
    ask_send_audio,
)


def inline_button_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    user_first_name = query.from_user.first_name
    current_stage = db_handler.get_current_stage(user_id)
    request_type = db_handler.get_request_type(user_id)

    if not current_stage or not request_type:
        if user_id not in interlinks.ADMIN_TELEGRAM_IDS:
            no_active_session_notification(user_id=user_id)
            return

    # Check stages
    if current_stage == "quote_enabled":
        if query.data == "quote_enabled":
            query.answer()
            query.edit_message_text(text=f"'Коробка-цитата' нужна.")
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"quote_enabled": True}
            )
            db_handler.set_user_stage(user_id, "quote_text")
            ask_quote_text(user_id=user_id)

        elif query.data == "quote_disabled":
            query.answer()
            query.edit_message_text(text=f"'Коробка-цитата' НЕ нужна.\n__________")
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"quote_enabled": False}
            )
            db_handler.set_user_stage(user_id, "audio_enabled")
            ask_audio_enabled(user_id=user_id)

        else:
            return
    elif current_stage == "quote_author_enabled":
        if query.data == "quote_author_enabled":
            query.answer()
            query.edit_message_text(text=f"Автор цитаты нужен.")
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"quote_author_enabled": True}
            )
            db_handler.set_user_stage(user_id, "quote_author_text")
            ask_quote_author_text(user_id=user_id)

        if query.data == "quote_author_disabled":
            query.answer()
            query.edit_message_text(text=f"Автор цитаты не нужен.\n__________")
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"quote_author_enabled": False}
            )
            db_handler.set_user_stage(user_id, "audio_enabled")
            ask_audio_enabled(user_id=user_id)
    elif current_stage == "bg_animation_type":
        if query.data == "bg_animation_scroll":
            query.answer()
            query.edit_message_text(text="Тип анимации заднего фона: SCROLL")
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "bg_animation_type": "scroll",
                    "fg_animation_type": "scroll",
                    "is_two_layer": False,
                },
            )
        elif query.data == "bg_animation_zoom":
            query.answer()
            query.edit_message_text(text="Тип анимации заднего фона: ZOOM")
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "bg_animation_type": "zoom",
                    "fg_animation_type": "zoom",
                    "is_two_layer": False,
                },
            )

        db_handler.set_user_stage(user_id, "send_bg")
        ask_send_bg(user_id)
    elif current_stage == "fg_enabled":
        if query.data == "fg_enabled":
            query.answer()
            query.edit_message_text(text="Передний план: Да")
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"fg_enabled": True, "is_two_layer": True}
            )
            db_handler.set_user_stage(user_id, "send_fg")
            ask_send_fg(user_id)
        elif query.data == "fg_disabled":
            query.answer()
            query.edit_message_text(text="Передний план: Нет\n__________")
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"fg_enabled": False}
            )
            db_handler.set_user_stage(user_id, "quote_enabled")
            ask_quote_enabled(user_id)
    elif current_stage == "fg_animation_type":
        if query.data == "fg_animation_facebook":
            query.answer()
            query.edit_message_text(
                text="Тип анимации переднего плана: Facebook\n__________"
            )
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"fg_animation_type": "facebook"}
            )

        elif query.data == "fg_animation_instagram":
            query.answer()
            query.edit_message_text(
                text="Тип анимации переднего плана: Instagram\n__________"
            )
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"fg_animation_type": "photo"}
            )

        elif query.data == "fg_animation_document":
            query.answer()
            query.edit_message_text(
                text="Тип анимации переднего плана: Document\n__________"
            )
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"fg_animation_type": "document"}
            )
            db_handler.set_user_stage(user_id, "quote_enabled")
            ask_quote_enabled(user_id)
            return

        db_handler.set_user_stage(user_id, "round_corners_enabled")
        ask_round_corners_enabled(user_id)

    elif current_stage == "round_corners_enabled":
        if query.data == "round_corners_enabled":
            query.answer()
            query.edit_message_text(
                text="Закругленные края переднего плана: Да\n__________"
            )
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"round_corners_enabled": True}
            )
        elif query.data == "round_corners_disabled":
            query.answer()
            query.edit_message_text(
                text="Закругленные края переднего плана: Нет\n__________"
            )
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"round_corners_enabled": False}
            )

        db_handler.set_user_stage(user_id, "quote_enabled")
        ask_quote_enabled(user_id)

    elif current_stage == "audio_enabled":
        if query.data == "audio_enabled":
            query.answer()
            query.edit_message_text(text=f"Аудио-файл есть.")
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"audio_enabled": True}
            )
            db_handler.set_user_stage(user_id=user_id, stage="send_audio")
            ask_send_audio(user_id)

        elif query.data == "audio_disabled":
            query.answer()
            query.edit_message_text(text=f"Аудио-файла нет.\n__________")
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"audio_enabled": False}
            )
            db_handler.set_user_stage(user_id=user_id, stage="check")
            check_results(user_id)

    elif current_stage == "check":
        if query.data == "results_correct":
            query.answer()
            query.edit_message_text(
                text=query.message.text + f"\n\nРезультаты верны.",
                disable_web_page_preview=True,
            )

            db_query = db_handler.get_active_entry_data(user_id=user_id)
            render_filename = f"{str(user_first_name)}-gfx-{int(time.time())}.mp4"
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "render_filename": render_filename,
                    "chat_id": user_id,
                    "status": "processing",
                },
            )

            # if quote is enabled send quote text and quote author to text editor (shavkat or sergey)
            testing = False
            if testing:
                if db_query["quote_enabled"]:

                    bot.send_message(
                        chat_id=user_id,
                        text="Заказ принят. Текст цитаты отправлен на проверку редактору. Скоро пришлю тебе файл(ы). Подожди, пожалуйста.\n__________",
                        reply_markup=ReplyKeyboardRemove(),
                        parse_mode=ParseMode.HTML,
                    )

                    # add quote to unchecked quotes
                    db_handler.update_doc_db_parameters(
                        doc_id=db_query.doc_id,
                        parameters={
                            "chat_id": db_query["telegram_id"],
                            "stage": "check_quote",
                            "qc_quote_checked": False,
                            "qc_main_notification_sent": False,
                            "qc_main_notification_responded": False,
                            "qc_text_notification_sent": False,
                            "qc_text_notification_responded": False,
                            "qc_author_notification_sent": False,
                            "qc_author_notification_responded": False,
                            "qc_final_notification_sent": False,
                            "qc_final_notification_responded": False,
                        },
                    )
                    # check_quotes()
                    return

            # if quote is disabled - start processing the order
            bot.send_message(
                chat_id=user_id,
                text="Заказ принят. Скоро пришлю тебе файл(ы). Подожди, пожалуйста.\n__________",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode=ParseMode.HTML,
            )

            process_order(db_query)

        elif query.data == "results_incorrect":
            query.answer()
            query.edit_message_text(
                text=query.message.text + f"\n\nРезультаты НЕ верны.",
                disable_web_page_preview=True,
            )
            bot.send_message(
                chat_id=user_id,
                text="Заказ отменен. Можешь оформить новый через /start.",
                reply_markup=ReplyKeyboardRemove(),
            )
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"status": "user_terminated_results"}
            )
            return

    elif current_stage == "readtime_set_speed":
        db_query = db_handler.get_active_entry_data(user_id=user_id)
        readtime_text = db_query["readtime_text"]
        readtime_text_message_id = db_query["readtime_text_message_id"]

        if query.data == "slow_readtime":
            readtime_time = calc_readtime(text=readtime_text, wpm=150)
            selected_speed_string = 0
        elif query.data == "medium_readtime":
            readtime_time = calc_readtime(text=readtime_text, wpm=160)
            selected_speed_string = 1
        elif query.data == "fast_readtime":
            readtime_time = calc_readtime(text=readtime_text, wpm=170)
            selected_speed_string = 2

        speed_text = query.message.reply_markup.inline_keyboard[0][
            selected_speed_string
        ]["text"]

        query.edit_message_text(
            text=query.message.text + f"\n{speed_text}.", disable_web_page_preview=True
        )
        bot.send_message(
            chat_id=user_id,
            text=f"<b>{readtime_time}</b> мин:сек - <i>хрон текста на скорости '{speed_text.lower()}'</i>",
            reply_to_message_id=readtime_text_message_id,
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
        )

        db_handler.update_db_parameters(
            user_id=user_id,
            parameters={
                "stage": "completed",
                "readtime_time": readtime_time,
                "status": "success",
            },
        )
    # elif current_stage == "readtime_set_speed":
    #     pass

    else:
        if "terminate_order" in query.data:
            doc_id = int(query.data[16:])
            db_handler.update_doc_db_parameters(
                doc_id=doc_id, parameters={"status": "tg_admin_terminated"}
            )
            query.edit_message_text(
                text=query.message.text + "\n\n TERMINATED",
                disable_web_page_preview=True,
            )

        elif "approve" in query.data:
            user_id = int(query.data.split()[1])
            db_handler.set_user_permission(user_id=user_id, permission=True)
            response = "approved"
            query.answer()
            query.edit_message_text(text=f"{user_id} {response}")
        elif "block" in query.data:
            user_id = int(query.data.split()[1])
            db_handler.set_user_permission(user_id=user_id, permission=False)
            response = "blocked"
            query.answer()
            query.edit_message_text(text=f"{user_id} {response}")
