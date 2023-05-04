# get env vars
import os

IS_DOCKER = os.environ.get("IS_DOCKER")

JWT_SECRET = os.environ.get("JWT_SECRET")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
REGISTER_PASSPHRASE = os.environ.get("REGISTER_PASSPHRASE")

BOT_ADMIN = os.environ.get("BOT_ADMIN")
BOT_ADMIN_PASSWORD = os.environ.get("BOT_ADMIN_PASSWORD")
BOT_ADMIN_EMAIL = os.environ.get("BOT_ADMIN_EMAIL")
