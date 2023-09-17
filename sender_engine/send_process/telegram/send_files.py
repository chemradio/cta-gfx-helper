import traceback
from pathlib import Path

import requests

from config import SEND_DOCUMENT_TELEGRAM_API_ENDPOINT
from send_process.gather_files import gather_files_from_storage


def send_files_raw(order: dict, user_id: int):
    send_successes = list()
    files_to_send = gather_files_from_storage(order)
    for file in files_to_send:
        try_count = 3
        while try_count:
            try:
                send_file_raw(
                    file,
                    user_id,
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


def send_file_raw(file_tuple: dict[str, bytes], receiver_id: int) -> None:
    files = {"document": file_tuple}

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
