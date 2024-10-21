from io import BytesIO

import requests


def download_order_file(filename: str, container_url: str) -> BytesIO:
    r = requests.get(container_url, json={"filename": filename})
    return BytesIO(r.content)


def delete_order_file(filename: str, container_url: str) -> None:
    r = requests.delete(container_url, json={"filename": filename})
    assert r.status_code == 200


def download_and_delete_order_file(filename: str, container_url: str) -> BytesIO:
    download_tries = 3
    while download_tries > 0:
        try:
            file = download_order_file(filename, container_url)
            delete_order_file(filename, container_url)
            return file
        except Exception:
            download_tries -= 1
    else:
        raise Exception("Failed to download file. Deletion aborted.")
