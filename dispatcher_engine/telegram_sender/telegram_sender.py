import tempfile

import requests

import config


class TelegramSender:
    @classmethod
    async def send_order(cls, order: dict) -> None:
        recipient_telegram_id = order["user"]["telegram_id"]

        # fetch files based on the order type
        files_to_send = await cls._gather_files(order)

        # send optional finishing message to the user
        await cls._send_message("Your order is ready", recipient_telegram_id)

        for file in files_to_send:
            cls._send_file(file, recipient_telegram_id)

    @classmethod
    async def _gather_files(cls, order) -> list[bytes]:
        request_type = order["request_type"]
        files = list()

        match request_type:
            case "video_auto":
                video_gfx_name: str = order["video_gfx_name"]
                file = await cls._fetch_file_from_storage(video_gfx_name)
                files.append(file)

            case "video_files":
                video_gfx_name: str = order["video_gfx_name"]
                file = await cls._fetch_file_from_storage(video_gfx_name)
                files.append(file)

            case "only_screenshots":
                cases = ("background_name", "foreground_name")
                for filename in cases:
                    file = await cls._fetch_file_from_storage(filename)
                    if file:
                        files.append(file)
            case _:
                return []

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
    async def _send_file(cls, file: bytes, recipient_telegram_id: int) -> None:
        files = {"document": file}
        kwargs = {
            "chat_id": recipient_telegram_id,
            "caption": "✅ Твой заказ готов.",
            "disable_content_type_detection": True,
            "allow_sending_without_reply": True,
        }
        r = requests.post(config.TELEGRAM_SEND_DOCUMENT_API, params=kwargs, files=files)
        r.raise_for_status()
