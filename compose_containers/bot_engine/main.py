import time
from pathlib import Path

from telegram.ext import Application

from telegram_bot.all_handler import AllHandler
from telegram_bot.bot_instance import BOT_TOKEN
from telegram_bot.callbacks.main_callback.main_dispatcher_callback import (
    dispatcher_callback,
)


def create_volume_folders():
    volume_path = Path().cwd() / "volume"

    children = (
        "cookie_file",
        "html_assemblies",
        "screenshots",
        "user_files",
        "video_exports",
    )
    children_paths = [volume_path / child for child in children]
    for child_path in children_paths:
        child_path.mkdir(parents=True, exist_ok=True)


def main():
    create_volume_folders()
    while True:
        try:
            application = Application.builder().token(BOT_TOKEN).build()
            application.add_handler(AllHandler(dispatcher_callback))
            application.run_polling()
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == "__main__":
    main()
