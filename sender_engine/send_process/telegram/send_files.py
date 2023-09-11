import traceback
from pathlib import Path

import config
import requests
from bot_instance import bot
from send_process.gather_files import gather_file_paths
from telegram import ReplyKeyboardRemove


def send_files_raw(order):
    send_successes = list()
    files_to_send = gather_file_paths(order)
    for file in files_to_send:
        try_count = 3
        while try_count:
            try:
                send_file_raw(
                    file,
                    order["user_telegram_id"],
                )
                send_successes.append(True)
                break

            except Exception as e:
                print("Failed to send file.")
                print(str(e))
                traceback.print_exc()
                try_count -= 1
        else:
            send_successes.append(False)

    return all(send_successes)


def send_file_raw(file: Path, receiver_id: int) -> None:
    assert file.is_file()
    file_size_mb = file.stat().st_size / 1024 / 1024

    print(f"{file_size_mb=}")
    assert file_size_mb < 49

    files = {"document": open(file, "rb")}
    kwargs = {
        "chat_id": receiver_id,
        "caption": "✅ Твой заказ готов.",
        "disable_content_type_detection": True,
        "allow_sending_without_reply": True,
    }
    r = requests.post(
        config.SEND_DOCUMENT_TELEGRAM_API_ENDPOINT, params=kwargs, files=files
    )
    result = r.json()
    print(result)

    assert result["ok"] == True
    assert "document" in result["result"]
