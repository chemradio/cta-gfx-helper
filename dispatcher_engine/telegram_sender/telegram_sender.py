import tempfile
from pprint import pprint

import requests

import config
from db_tortoise.orders_models import Order


class TelegramSender:
    @classmethod
    async def send_order(cls, order: Order) -> None:
        await order.fetch_related("user")

        recipient_telegram_id = order.user.telegram_id

        if order.error:
            return await cls._report_error_to_user(order, recipient_telegram_id)

        # fetch files based on the order type
        files_to_send = await cls._gather_files(order)

        for file_tuple in files_to_send:
            await cls._send_file(file_tuple, recipient_telegram_id)

    @classmethod
    async def _gather_files(cls, order: Order) -> list[tuple[str, bytes]]:
        match order.request_type:
            case "video_auto":
                filetypes = ("video_gfx_name",)
            case "video_files":
                filetypes = ("video_gfx_name",)
            case "only_screenshots":
                filetypes = ("background_name", "foreground_name")
            case _:
                return []

        files = list()
        for filetype in filetypes:
            filename = getattr(order, filetype)
            file_bytes = await cls._fetch_file_from_storage(filename)
            if file_bytes:
                files.append((filename, file_bytes))

        return files

    @classmethod
    async def _fetch_file_from_storage(cls, filename: str) -> bytes:
        r = requests.get(config.STORAGE_UNIT_URL, params={"filename": filename})
        if r.status_code != 200:
            return None
        return r.content

    @classmethod
    async def _send_message(cls, message: str, recipient_telegram_id: int) -> None:
        kwargs = {"chat_id": recipient_telegram_id, "text": message}
        r = requests.post(config.TELEGRAM_SEND_MESSAGE_API, params=kwargs)

    @classmethod
    async def _send_file(
        cls, file_tuple: dict[bytes], recipient_telegram_id: int
    ) -> None:
        files = {"document": file_tuple}
        kwargs = {
            "chat_id": recipient_telegram_id,
            "caption": "✅ Твой заказ готов.",
            "disable_content_type_detection": True,
            "allow_sending_without_reply": True,
        }
        r = requests.post(config.TELEGRAM_SEND_DOCUMENT_API, params=kwargs, files=files)
        r.raise_for_status()

    @classmethod
    async def _report_error_to_user(
        cls, order: Order, recipient_telegram_id: int
    ) -> None:
        message = f"Произошла ошибка. Пожалуйста, перешли это сообщение администратору.\n\n{dict(order)}"
        kwargs = {"chat_id": recipient_telegram_id, "text": message}
        r = requests.post(config.TELEGRAM_SEND_MESSAGE_API, params=kwargs)
