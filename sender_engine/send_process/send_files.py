import traceback
from pathlib import Path

import requests
from telegram import ReplyKeyboardRemove

import config
from bot_instance import bot
from send_process.gather_files import gather_file_paths


async def send_files(order):
    send_successes = list()

    files_to_send = gather_file_paths(order)

    for file in files_to_send:
        with open(file, "rb") as binarified_file:
            try_count = 3
            while try_count:
                try:
                    await bot.send_document(
                        chat_id=order["user_telegram_id"],
                        document=binarified_file,
                        caption="✅ Твой заказ готов.",
                        # reply_to_message_id=order["results_message_id"],
                        allow_sending_without_reply=True,
                        reply_markup=ReplyKeyboardRemove(),
                        read_timeout=300,
                        write_timeout=300,
                        pool_timeout=300,
                        connect_timeout=300,
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
    files = {"document": open(file, "rb")}
    kwargs = {
        "chat_id": receiver_id,
        "caption": "✅ Твой заказ готов.",
    }
    r = requests.post(
        config.SEND_DOCUMENT_TELEGRAM_API_ENDPOINT, params=kwargs, files=files
    )
