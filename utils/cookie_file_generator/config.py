from pathlib import Path

logged_in_to_social_websites = False
LOGIN_REQUIRED = ("facebook", "twitter", "instagram")

SOCIAL_WEBSITES = {
    "facebook": "https://facebook.com",
    "twitter": "https://twitter.com",
    "instagram": "https://instagram.com",
}

COOKIE_FILE_PATH = Path().cwd() / "cookie_file.json"
COPY_COOKIE_TO_DEV = True

DEV_COOKIE_FILE_PATH = (
    Path().cwd().parent.parent
    / "dev"
    / "volume"
    / "asset_storage"
    / "cookie_file"
    / "cookie_file.json"
)
