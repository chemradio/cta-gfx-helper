import os
from pathlib import Path

import requests

ON_CLIENT = Path(os.path.dirname(__file__)) / "store" / "on_client"
ON_SERVER = Path(os.path.dirname(__file__)).parent / "store"
FROM_SERVER = Path(os.path.dirname(__file__)) / "store" / "from_server"
API = "http://127.0.0.1:9010/"


def gather_files(path: Path) -> list:
    return list(path.glob("*"))


def get_file(filename: str | Path) -> None:
    print("getting file:", filename)
    # send get request for file
    r = requests.get(API, params={"filename": filename})
    with open(FROM_SERVER / filename, "wb+") as f:
        f.write(r.content)


def store_file(filename: str | Path) -> None:
    print("storing file:", filename)
    # send post request with file to the api
    requests.post(
        API,
        files={"upload_file": open(filename, "rb")},
        data={"category": "screenshots"},
    )


def send_files():
    client_files = gather_files(ON_CLIENT)
    for file in client_files:
        store_file(file)


def get_files():
    server_files = gather_files(ON_SERVER)
    for file in server_files:
        get_file(file.name)


def main():
    # send_files()
    get_files()


if __name__ == "__main__":
    main()
