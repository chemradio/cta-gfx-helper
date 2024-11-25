import httpx


async def notify_dispatcher(dispatcher_url: str, notification: dict):
    with httpx.Client() as client:
        await client.post(dispatcher_url, json=notification)
