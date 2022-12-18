import asyncio
import traceback

from telegram import ReplyKeyboardRemove

from bot_instance import bot


async def send_order(order: dict) -> bool:

    # get order type
    request_type = order.get("request_type")
    files_to_send = list()

    match request_type:
        case "only_screenshots":
            assets = ("bg_path", "fg_path")
        case "video_auto":
            assets = ("render_output_path",)
        case "video_files":
            assets = ("render_output_path",)
        case _:
            return False

    files_to_send = [order.get(asset) for asset in assets if order.get(asset)]

    for file in files_to_send:
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
