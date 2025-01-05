import asyncio

import httpx


async def check_order_status(container_url: str, order_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(container_url, params={"order_id": order_id})
        return r.json()


async def poll_order_status_finished(container_url: str, order_id: str) -> dict:
    while True:
        order_data = await check_order_status(container_url, order_id)
        if order_data.get("status") == "finished":
            return order_data
        await asyncio.sleep(3)
