from container_interaction.gather_orders import get_ready_to_send_order
from send_process.send_order import send_order
from container_interaction.edit_order_db import mark_order_sent


def orders_sender():
    while True:
        order = get_ready_to_send_order()
        print(f"{__name__}:{order=}")
        if not order:
            break

        send_success = send_order(order)
        mark_order_sent(order, send_success)
