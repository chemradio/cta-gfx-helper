from telegram import Update
from telegram.ext import ContextTypes
import traceback

# from config import Readspeed
from container_interaction.orders import send_order_to_dispatcher
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder
from py_gfxhelper_lib.readtime import calc_readtime, Readspeed


async def readtime_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # raise Exception("Not implemented")
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    # initialize order / ask text
    if stage == "start_order":
        user_data.update({"stage": "readtime_text"})
        return await Responder.readtime.ask_readtime_text(user_id)

    if stage == "readtime_text":
        if not update.message.text:
            return await Responder.readtime.bad_text(user_id)
        user_data.update(
            {"stage": "readtime_speed", "readtime_text": update.message.text}
        )
        return await Responder.readtime.ask_readtime_speed(user_id)

    if stage == "readtime_speed":
        try:
            speed_map = {
                "slow_readtime": Readspeed.SLOW,
                "medium_readtime": Readspeed.MEDIUM,
                "fast_readtime": Readspeed.FAST,
            }
            trans_map = {
                "slow_readtime": "медленно",
                "medium_readtime": "средне",
                "fast_readtime": "быстро",
            }
            callback_data = update.callback_query.data
            await update.callback_query.answer(cache_time=180)
            await update.callback_query.edit_message_text(
                text=f"📝 Скорость чтения: {trans_map[callback_data]}."
            )

            readspeed = speed_map[callback_data]
            readtime = calc_readtime(user_data["readtime_text"], readspeed)

            user_data.update({"readtime_speed": readspeed})
            user_data.update({"readtime_result": readtime})

            await Responder.readtime.readtime_results(
                user_id, readtime, readspeed.value
            )
            user_data.clear()

        except Exception as e:
            # print traceback

            traceback.print_exc()
            await Responder.errors.gp_error(user_id)
            await Responder.errors.custom_error(user_id, str(e))
            return await Responder.readtime.ask_readtime_speed(user_id)
