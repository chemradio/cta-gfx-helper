async def filter_finished_orders(orders: list[dict]) -> list[dict]:
    return [order for order in orders if order["status"] == "finished"]


async def filter_failed_orders(orders: list[dict]) -> list[dict]:
    return [order for order in orders if order["error"] == True]
