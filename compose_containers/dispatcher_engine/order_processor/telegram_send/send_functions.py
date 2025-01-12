import os
from io import BytesIO
import httpx

BOT_TOKEN = os.getenv("BOT_TOKEN")
SEND_DOCUMENT_TELEGRAM_API_ENDPOINT = (
    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
)


async def send_file_telegram(
    filename: str, file_bytes: BytesIO, receiver_id: int
) -> dict:
    if not check_filesize(file_bytes):
        print(
            f"Attention! File size exceeds 25 MB: {len(file_bytes.getvalue()) / 1024 / 1024} MB",
        )

    files = {"document": (filename, file_bytes)}

    kwargs = {
        "chat_id": receiver_id,
        "caption": "✅ Твой заказ готов.",
        "disable_content_type_detection": True,
        "allow_sending_without_reply": True,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(
            SEND_DOCUMENT_TELEGRAM_API_ENDPOINT, params=kwargs, files=files
        )
    r.raise_for_status()

async def send_text_telegram(text: str, receiver_id: int) -> dict:
    kwargs = {
        "chat_id": receiver_id,
        "text": text,
    }
    async with httpx.AsyncClient() as client:
        r = await client.post(SEND_DOCUMENT_TELEGRAM_API_ENDPOINT, params=kwargs)
    r.raise_for_status()


# function for checking if filezise exceeds 25 mb
def check_filesize(file_bytes: BytesIO) -> bool:
    file_size = len(file_bytes.getvalue())
    file_bytes.seek(0)
    return file_size < 25 * 1024 * 1024
