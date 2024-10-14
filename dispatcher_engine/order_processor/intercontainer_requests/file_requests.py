from io import BytesIO

import requests


def download_order_file(filename: str, container_url: str) -> BytesIO:
    r = requests.get(container_url, json={"filename": filename})
    return BytesIO(r.content)


def delete_order_file(filename: str, container_url: str) -> None:
    r = requests.delete(container_url, json={"filename": filename})
    assert r.status_code == 200
