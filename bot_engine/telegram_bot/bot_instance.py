import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    BOT_TOKEN = input("Please enter bot token: ")

from telegram import Bot

bot = Bot(token=BOT_TOKEN)
