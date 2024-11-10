import asyncio

import httpx


async def check_order_status(order_id: str, container_url: str) -> dict:
    async with httpx.AsyncClient() as client:
        r = await client.get(container_url, json={"order_id": order_id})
        return r.json()


async def poll_order_status_finished(order_id: str, container_url: str) -> dict:
    while True:
        order_status = await check_order_status(order_id, container_url)
        if order_status["status"] == "finished":
            return order_status
        await asyncio.sleep(3)
