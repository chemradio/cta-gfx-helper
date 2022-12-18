import time

from bot_instance import bot
from config import BOT_ADMIN
from container_interaction.edit_order_db import mark_order_sent
from container_interaction.gather_orders import get_ready_to_send_order
from send_process.send_order import send_order


async def orders_sender():
    while True:
        order = get_ready_to_send_order()
        print(f"{__name__}:{order=}")
        if not order:
            print("No more orders to send.")
            break

        send_success = await send_order(order)
        if not send_success:
            await bot.send_message(BOT_ADMIN, f"Failed to send order\n\n{order}")

        mark_success = await mark_order_sent(order, send_success)

        if not mark_success:
            await bot.send_message(
                BOT_ADMIN, f"Failed to mark sent order\n{send_success=}\n\n{order=}"
            )

        time.sleep(3)

    return True
