import httpx

from config import ORDERS_ENDPOINT


async def add_order_to_db(telegram_id: int, user_data: dict) -> bool:
    files = {
        k: v
        for k in ("background_file", "foreground_file", "audio_file")
        if (v := user_data.pop(k)) is not None
    }

    user_data.update({"telegram_id": telegram_id, "ordered_from": "telegram"})

    user_data.pop("results_correct", None)
    user_data.pop("results_message", None)

    print(f"{user_data=}", flush=True)

    async with httpx.AsyncClient() as client:
        r = await client.post(ORDERS_ENDPOINT, data=user_data, files=files)
        return r.json()


# async def fetch_orders(status: str = None) -> list:
#     r = requests.get(
#         f"{DISPATCHER_ORDERS_ENDPOINT}", json={"status": status} if status else {}
#     )
#     return r.json()


# async def cancel_order(order_id: int) -> bool:
#     r = requests.put(
#         f"{DISPATCHER_ORDERS_ENDPOINT}/{order_id}",
#         json={"status": "admin_cancelled"},
#     )
#     json = r.json()
#     return True