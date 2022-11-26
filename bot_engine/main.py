import time
from telegram_bot.main_dispatcher import bot_application_v20


def main():
    while True:
        try:
            print("starting the bot")
            bot_application_v20()
        except Exception as e:
            print(e)
            time.sleep(5)


if __name__ == "__main__":
    main()
