from pathlib import Path

import requests

from config import BOT_ADMIN, BOT_TOKEN


def raw_send(file: Path, receiver_id: int) -> None:
    api_endpoint = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    files = {"document": open(file, "rb")}
    kwargs = {"chat_id": receiver_id}
    r = requests.post(api_endpoint, params=kwargs, files=files)


def main():
    filepath = Path.cwd() / "requirements.txt"
    raw_send(filepath, BOT_ADMIN)


if __name__ == "__main__":
    main()
