import os

import requests
from config import DISPATCHER_NODE_URL

admin_orders_api = f"{DISPATCHER_NODE_URL}/admin/db_manipulation/orders"


def fetch_all_active_orders() -> list:
    response = requests.get(admin_orders_api, json={"status": "active"})
    return response.json()
