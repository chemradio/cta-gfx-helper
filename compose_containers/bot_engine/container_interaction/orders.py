import httpx
from pprint import pprint
from config import ORDERS_ENDPOINT
from py_gfxhelper_lib.order_enums import OrderSource, OrderStatus


async def send_order_to_dispatcher(telegram_id: int, user_data: dict) -> bool:
    files = {
        k: (asset_file.filename, asset_file.bytesio)
        for k in ("background_file", "foreground_file", "audio_file")
        if (asset_file := user_data.pop(k, None)) is not None
    }
    user_data.update({"telegram_id": telegram_id, "ordered_from": "telegram"})
    user_data.pop("results_correct", None)
    user_data.pop("results_message", None)
    print(f"{user_data=}")

    async with httpx.AsyncClient() as client:
        r = await client.post(
            ORDERS_ENDPOINT, data=user_data, files=files if files else None
        )
        return r.json()


async def fetch_orders(
    telegram_id: int | None = None,
    email: str | None = None,
    status: OrderStatus | None = None,
    ordered_from: OrderSource | None = None,
) -> list[dict | None]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{ORDERS_ENDPOINT}list/",
            params={
                "telegram_id": telegram_id,
                "email": email,
                "status": status,
                "ordered_from": ordered_from,
            },
        )
    return r.json()


# async def cancel_order(order_id: int) -> bool:
#     r = requests.put(
#         f"{DISPATCHER_ORDERS_ENDPOINT}/{order_id}",
#         json={"status": "admin_cancelled"},
#     )
#     json = r.json()
#     return True
