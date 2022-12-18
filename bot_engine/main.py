import time
from pathlib import Path

from telegram_bot.main_dispatcher import bot_application_v20


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
            print("starting the bot")
            bot_application_v20()
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == "__main__":
    main()
