import time

from config import BOT_ADMIN
from container_interaction.helpers import UserStatus
from container_interaction.orders_db import fetch_orders
from telegram_bot.responders.main_responder import Responder


async def list_10_orders_to_admin() -> None:
    print("listing 10")
    all_orders = await fetch_orders()
    if not all_orders:
        return None

    last_ten_orders = all_orders[:10]
    last_ten_orders = all_orders[-10:]

    for order in last_ten_orders:
        from pprint import pprint

        pprint(order)
        wait_secs = time.time() - order.get("order_creation_end_timestamp")
        wait_time = time.strftime("%H:%M:%S", time.gmtime(wait_secs))
        customer_name = "... to be implemented"
        order.update({"wait_time": wait_time, "customer_name": customer_name})
        return await Responder.admin_panel.list_single_order(BOT_ADMIN, order)

    # users_list = await fetch_users()
    # target_user_group = [user for user in users_list if user["status"] == type.value]
    # if not target_user_group:
    #     return await Responder.register_admin.empty_users_list(BOT_ADMIN)

    # for user in target_user_group:
    #     await Responder.register_admin.list_user(
    #         admin_id=BOT_ADMIN,
    #         user_status=type,
    #         user_id=user["telegram_id"],
    #         first_name=user["first_name"],
    #     )


async def list_active_orders_to_admin() -> None:
    ...
