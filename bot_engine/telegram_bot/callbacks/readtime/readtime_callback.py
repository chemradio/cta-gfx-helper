from telegram import Update
from telegram.ext import ContextTypes

from config import Readspeed
from container_interaction.orders import add_order_to_db
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder
from telegram_bot.utils.calc_readtime import calc_readtime


async def readtime_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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
            await update.callback_query.answer(cache_time=180)
            await update.callback_query.edit_message_text(
                text=f"📝 Скорость чтения: {trans_map[update.callback_query.data]}."
            )
            readspeed: Readspeed = speed_map[update.callback_query.data]
            user_data.update({"readtime_speed": readspeed.value})

            readtime = calc_readtime(
                text=user_data["readtime_text"], wpm=user_data["readtime_speed"]
            )
            user_data.update({"readtime_result": readtime})

            await Responder.readtime.readtime_results(user_id, context)

            await add_order_to_db(user_id, user_data)
            user_data.clear()
        except:
            await Responder.errors.gp_error(user_id)
            return await Responder.readtime.ask_readtime_speed(user_id)
