from telegram import Update
from telegram.ext import ContextTypes
from telegram_bot.callbacks.main_callback.main_callback_helpers import parse_user_id
from telegram_bot.responders.main_responder import Responder
from .shared_callbacks import link_callback, results_callback
from container_interaction.orders import send_order_to_dispatcher


async def only_screenshots_callback(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    user_id = parse_user_id(update)
    user_data = context.user_data
    stage = user_data.get("stage")

    # initialize order / ask LINK
    if stage == "start_order":
        user_data.update({"stage": "link"})
        return await Responder.link.ask_link(user_id)

    # handle LINK response
    if stage == "link":
        return await link_callback(update, context, only_screenshots_callback)

    # ask results
    if stage == "link_passed":
        user_data.update({"stage": "results"})
        return await Responder.results.show_results(user_id, user_data)

    # handle RESULTS response
    if stage == "results":
        return await results_callback(update, context, only_screenshots_callback)

    # finish order creation
    if stage == "results_confirmed":
        await send_order_to_dispatcher(user_id, user_data)
        user_data.clear()
        return await Responder.results.results_correct(user_id)
