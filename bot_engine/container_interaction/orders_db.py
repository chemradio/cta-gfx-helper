import requests
from config import ADD_ORDER_ENDPOINT


async def add_order_to_db(telegram_id: int, user_data: dict) -> bool:
    print(f"{telegram_id=}, {user_data=}")
    user_data.update({"telegram_id": telegram_id})
    user_data.pop("results_correct", None)

    print(f"{user_data=}")

    r = requests.post(ADD_ORDER_ENDPOINT, json=user_data)
    print(r.status_code)
    print(r.json())

    return True
