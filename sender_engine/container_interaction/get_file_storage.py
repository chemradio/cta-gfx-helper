import requests

from config import STORAGE_UNIT_URL


def fetch_file_from_storage(filename: str) -> bytes:
    r = requests.get(STORAGE_UNIT_URL, params={"filename": filename})
    if r.status_code != 200:
        return None
    return r.content
