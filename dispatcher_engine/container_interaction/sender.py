import asyncio

from config import SENDER_ENDPOINT
from db_tortoise.helper_enums import OrderSource
from db_tortoise.orders_models import Order
from telegram_sender.telegram_sender import TelegramSender


async def signal_to_sender(order: Order):
    if order.ordered_from == OrderSource.TELEGRAM:
        print("sending telegram order now!!!")
        return await TelegramSender.send_order(order)
