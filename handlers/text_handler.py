import interlinks

from engines.telegram_bot.bot_instance import bot


from engines.utils import check_is_url
from database.db import db_handler
from telegram import (
    ReplyKeyboardRemove,
    Update,
    ParseMode,
)
from telegram.ext import (
    CallbackContext,
)


from handlers.decorators import logger_bot

from handlers.attachment_handler import attachment_handler
from handlers.error_responses import (
    no_active_session_notification,
    wrong_link_notification,
    gp_error_notification,
    try_again_error,
)
from handlers.question_senders import (
    ask_readtime_speed,
    ask_quote_author_enabled,
    ask_quote_enabled,
    ask_audio_enabled,
    

)

from handlers.check_results import check_results


################################################################
# Main message handler
################################################################
def main_handler(update: Update, _: CallbackContext) -> None:
    if update.to_dict()["message"].get("reply_to_message"):
        if (
            "photo"
            or "document"
            or "audio" in update.to_dict()["message"]["reply_to_message"]
        ):
            logger_bot.debug(
                f"Main Handler - reply detected - redirecting to attachment handler"
            )
            attachment_handler(update, _)
            return

    ### GET BASIC USER INFO ###
    user_id = update.message.from_user.id
    db_id = db_handler.get_active_doc_id(user_id)
    if not db_id:  # check if the session expired first
        no_active_session_notification(user_id)
        return

    # get current stage to define what to ask from the user
    current_stage = db_handler.get_current_stage(user_id)
    request_type = db_handler.get_request_type(user_id)

    if current_stage == 'awaiting_announcement':
        announcement = update.message.text
        registered_users = db_handler.get_registered_users()
        # registered_users = [{'user':'tim', 'telegram_id': 247066990},]
        for user in registered_users:
            try:
                bot.send_message(
                    chat_id=user['telegram_id'],
                    text=f"""<b>Рассылка от администратора.</b>\n\n<i>{announcement}</i>\n\nПо всем вопросам - пишите @chemradio""",
                    parse_mode=ParseMode.HTML,
                )
            except:
                ...
        db_handler.terminate_all_sessions(update.message.from_user.id)
        return

    logger_bot.debug(
        f"Main Handler for {update.message.from_user.first_name} {user_id}, request_type: {request_type}, stage {current_stage}"
    )

    if request_type == "readtime":
        if update.message.text:
            message_id = update.message.message_id
            db_handler.update_db_parameters(
                user_id=user_id,
                parameters={
                    "readtime_text": update.message.text,
                    "stage": "readtime_set_speed",
                    "readtime_text_message_id": message_id,
                },
            )
            ask_readtime_speed(user_id)
            return
        else:
            gp_error_notification(user_id=user_id)
            return

    ### LINK STAGE ###
    if current_stage == "link":
        links = check_is_url(update.message.text)
        if links:
            ### DETERMINE LINK TYPE - FB, TWI, IG, OR SCROLL ###
            if "fb.me" in update.message.text or "facebook" in update.message.text:
                animation_type = "facebook"
            elif "instagr" in update.message.text:
                animation_type = "instagram"
            elif "t.co" in update.message.text or "twitter" in update.message.text:
                animation_type = "twitter"
            elif '/t.me/' in update.message.text:
                animation_type = "telegram"
            else:
                animation_type = "scroll"
        else:
            wrong_link_notification(user_id)
            return

        ### PUSH THE LINK TO DB ###
        db_handler.update_db_parameters(
            user_id=user_id,
            parameters={"link": links[0], "animation_type": animation_type},
        )

        if request_type == "only_screenshots":
            db_handler.set_user_stage(user_id, "check")
            check_results(user_id=user_id)
            return

        elif request_type == "video_auto":
            db_handler.set_user_stage(user_id, "quote_enabled")
            ask_quote_enabled(user_id=user_id)
            return

    ### QUOTE TEXT ###
    elif current_stage == "quote_text":
        if update.message.text:
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"quote_text": update.message.text}
            )
            db_handler.set_user_stage(user_id, "quote_author_enabled")
            ask_quote_author_enabled(user_id)
            return
        else:
            try_again_error(user_id)
            return

    ### QUOTE AUTHOR NAME ###
    elif current_stage == "quote_author_text":
        if update.message.text:
            db_handler.update_db_parameters(
                user_id=user_id, parameters={"quote_author": update.message.text}
            )
            db_handler.set_user_stage(user_id, "audio_enabled")
            ask_audio_enabled(user_id)
            return
        else:
            try_again_error(user_id)
            return

    # ### AUDIO ENABLED ###
    # handled in inline query handler
    # elif current_stage == 'audio_enabled':
    #     pass

    ### AUDIO FILE SEND ###
    # handled in attachment handler

    ### CHECK RESULTS ###
    elif current_stage == "check":

        update.message.reply_text(
            "Пожалуйста, коснись нужного варианта.", reply_markup=ReplyKeyboardRemove()
        )
        return

    # final stages
    elif current_stage == "completed":
        update.message.reply_text(
            interlinks.stage_texts["common"]["start_new_session"],
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
        )
        return

    elif current_stage == "render" or "processing":
        update.message.reply_text(
            interlinks.stage_texts["common"]["wait_for_processing"],
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.HTML,
        )
        return

    else:
        update.message.reply_text(
            interlinks.stage_texts["weird_error"], parse_mode=ParseMode.HTML
        )
        return