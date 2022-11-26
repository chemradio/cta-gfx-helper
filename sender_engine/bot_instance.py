import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

from telegram import Bot

bot = Bot(token=BOT_TOKEN)
