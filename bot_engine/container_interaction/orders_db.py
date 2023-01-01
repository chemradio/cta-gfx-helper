import os

import requests

from config import ADD_ORDER_ENDPOINT, DISPATCHER_ORDERS_ENDPOINT
from telegram_bot.bot_instance import bot


async def add_order_to_db(telegram_id: int, user_data: dict) -> bool:
    user_data.update({"telegram_id": telegram_id})
    user_data.pop("results_correct", None)
    r = requests.post(ADD_ORDER_ENDPOINT, json=user_data)
    return True


async def fetch_orders(status: str = None) -> list:
    r = requests.get(f"{DISPATCHER_ORDERS_ENDPOINT}/list", json={"status": status})
    json = r.json()
    return json["orders"]


async def cancel_order(order_id: int) -> bool:
    r = requests.post(
        f"{DISPATCHER_ORDERS_ENDPOINT}/edit",
        json={"order_id": order_id, "status": "admin_cancelled"},
    )
    json = r.json()
    return True
