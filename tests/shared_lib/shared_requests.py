import httpx
from .files.asset_file import AssetFile
import asyncio


async def check_order(url: str, order_id: str) -> dict:
    async with httpx.Client() as client:
        response = client.get(url, params={"order_id": order_id})
        return response.json()


async def filter_finished_orders(orders: list[dict]) -> list[dict]:
    return [order for order in orders if order["status"] == "finished"]


async def filter_failed_orders(orders: list[dict]) -> list[dict]:
    return [order for order in orders if order["error"] == True]


async def download_file(url: str, filename: str) -> AssetFile:
    async with httpx.Client() as client:
        response = client.get(url + "/file_server", params={"filename": filename})
        return AssetFile(
            bytes=response.content,
            mime_type=response.headers["Content-Type"],
        )


async def poll_order_status_finished(url: str, order_id: str) -> dict:
    while True:
        order_data = await check_order(url, order_id)
        if order_data["status"] == "finished":
            return order_data
        await asyncio.sleep(3)


async def get_order_files(url: str, order_id: str) -> list[AssetFile | None]:
    order = await poll_order_status_finished(url, order_id)
    downloaded_files = []
    for file in order["output_filenames"]:
        asset_file = download_file(file, url)
        downloaded_files.append(asset_file)
    return downloaded_files
