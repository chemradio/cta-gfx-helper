from py_gfxhelper_lib.files import AssetFile
from .telegram_reporter.return_result import return_result_telegram


async def return_order_result_to_user(
    order: dict, container_output: list[AssetFile]
) -> bool:
    if order.get("telegram_id"):
        await return_result_telegram(
            telegram_id=order["telegram_id"],
            container_output=container_output,
        )
        return True

    return False
