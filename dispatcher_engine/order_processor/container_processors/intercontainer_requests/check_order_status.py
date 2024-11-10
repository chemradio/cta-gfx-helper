import asyncio
import json

import httpx


async def check_order_status(order_id: str, container_url: str) -> dict:
    print("checking order status")
    async with httpx.AsyncClient() as client:
        r = await client.get(container_url, params={"order_id": order_id})
        return r.json()


async def poll_order_status_finished(order_id: str, container_url: str) -> dict:
    print("polling order status")
    while True:
        order_data = await check_order_status(order_id, container_url)
        print(f"order status: {order_data['status']}")
        if order_data["status"] == "finished":
            print("returning poll order status finished", order_data)
            return order_data
        await asyncio.sleep(3)
