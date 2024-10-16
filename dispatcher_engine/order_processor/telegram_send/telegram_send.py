import os
from io import BytesIO

import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
SEND_DOCUMENT_TELEGRAM_API_ENDPOINT = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
)


def send_file_raw(filename: str, file_bytes: BytesIO, receiver_id: int) -> None:
    files = {"document": (filename, file_bytes.read())}

    kwargs = {
        "chat_id": receiver_id,
        "caption": "✅ Твой заказ готов.",
        "disable_content_type_detection": True,
        "allow_sending_without_reply": True,
    }
    r = requests.post(SEND_DOCUMENT_TELEGRAM_API_ENDPOINT, params=kwargs, files=files)
    r.raise_for_status()
    result = r.json()
    print(result)
