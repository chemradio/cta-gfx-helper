import os
from io import BytesIO

import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
SEND_DOCUMENT_TELEGRAM_API_ENDPOINT = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
)


def send_file_telegram(filename: str, file_bytes: BytesIO, receiver_id: int) -> dict:
    if not check_filesize(file_bytes):
        print(
            f"Attention! File size exceeds 25 MB: {len(file_bytes.getvalue()) / 1024 / 1024} MB",
        )

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
    return result


# function for checking if filezise exceeds 25 mb
def check_filesize(file_bytes: BytesIO) -> bool:
    return len(file_bytes.getvalue()) > 25 * 1024 * 1024
