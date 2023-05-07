import os

from helpers.passwords import generate_password


def populate_dict_with_env(env_dict) -> dict:
    env_dict["IS_DOCKER"] = True

    env_dict["REGISTER_PASSPHRASE"] = os.environ.get("REGISTER_PASSPHRASE")
    env_dict["BOT_TOKEN"] = os.environ.get("BOT_TOKEN")
    env_dict["BOT_ADMIN"] = os.environ.get("BOT_ADMIN")
    env_dict["BOT_ADMIN_PASSWORD"] = os.environ.get("BOT_ADMIN_PASSWORD")
    env_dict["BOT_ADMIN_EMAIL"] = os.environ.get("BOT_ADMIN_EMAIL")

    # autogenerate passwords if not found in environment
    env_dict["POSTGRES_PASSWORD"] = os.environ.get(
        "POSTGRES_PASSWORD", generate_password()
    )
    env_dict["JWT_SECRET"] = os.environ.get("JWT_SECRET", generate_password())
    return env_dict
