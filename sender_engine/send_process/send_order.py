import asyncio
import traceback

from telegram import ReplyKeyboardRemove

from bot_instance import bot
from send_process.gather_files import gather_file_paths


async def send_order(order: dict) -> bool:
    # get order type
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
                    return True
                except Exception as e:
                    print("Failed to send file.")
                    print(str(e))
                    traceback.print_exc()
                    try_count -= 1
            else:
                return False
