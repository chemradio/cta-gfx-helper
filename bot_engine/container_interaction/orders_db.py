import requests

from config import ADD_ORDER_ENDPOINT, DISPATCHER_ORDERS_ENDPOINT


async def add_order_to_db(telegram_id: int, user_data: dict) -> bool:
    print(f"{telegram_id=}, {user_data=}")
    user_data.update({"telegram_id": telegram_id})
    user_data.pop("results_correct", None)

    print(f"{user_data=}")

    r = requests.post(ADD_ORDER_ENDPOINT, json=user_data)
    print(r.status_code)
    print(r.json())

    return True


async def fetch_orders() -> list:
    r = requests.get(f"{DISPATCHER_ORDERS_ENDPOINT}/list", json={})
    json = r.json()
    return json["orders"]


async def cancel_order(order_id: int) -> bool:
    r = requests.post(
        f"{DISPATCHER_ORDERS_ENDPOINT}/edit",
        json={"order_id": order_id, "status": "admin_cancelled"},
    )
    json = r.json()
    return True
