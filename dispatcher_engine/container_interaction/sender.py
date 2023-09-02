import requests

from db_tortoise.helper_enums import OrderSource
from db_tortoise.orders_models import Order
from telegram_sender.telegram_sender import TelegramSender


async def signal_to_sender(order: Order):
    if order.ordered_from == OrderSource.TELEGRAM:
        try:
            return await TelegramSender.send_order(order)
        except Exception as e:
            order.error = True
            order.error_type = f"Send Error: {str(e)}"
            r = requests.put(
                "http://localhost:9000/intercontainer/orders",
                json=dict(order),
            )
