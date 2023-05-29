import os
from pathlib import Path

import requests

ON_CLIENT = Path(os.path.dirname(__file__)) / "store" / "on_client"
ON_SERVER = Path(os.path.dirname(__file__)) / "store" / "on_server"


def gather_files(path: Path) -> list:
    return list(path.glob("*"))


def get_file(filename: str | Path) -> None:
    print("getting file:", filename)
    # send get request for file


def store_file(filename: str | Path) -> None:
    print("storing file:", filename)
    # send post request with file to the api


def main():
    client_files = gather_files(ON_CLIENT)
    for file in client_files:
        store_file(file)


if __name__ == "__main__":
    main()
