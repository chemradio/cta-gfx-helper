import httpx

from py_gfxhelper_lib.constants import ContainerUrls


async def order_screenshots(
    screenshot_url: str,
    container_url: str = ContainerUrls.SCREENSHOOTER,
) -> str:
    async with httpx.AsyncClient() as client:
        r = await client.post(container_url, data={"screenshot_link": screenshot_url})
        return r.json()["order_id"]
