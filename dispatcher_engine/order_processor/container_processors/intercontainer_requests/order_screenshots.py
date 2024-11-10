import httpx

from . import CONTAINER_URLS


async def order_screenshots(
    screenshot_url: str,
    container_url: str = CONTAINER_URLS.Screenshoter,
) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(container_url, data={"screenshot_link": screenshot_url})
        return r.json()["order_id"]
