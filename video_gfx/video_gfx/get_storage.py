from pathlib import Path

import config
import requests


def get_file_from_storage_unit(filename: str) -> Path | None:
    """downloads file from the storage unit container based on the file's filename
    Then stores it in the volume / storage unit folder. This folder is then searched
    by other functions to get the filepath. Function also returns the path"""
    store_file_path = config.STORAGE_UNIT_FOLDER / filename

    r = requests.get(config.STORAGE_UNIT_URL, params={"filename": filename})
    if r.status_code != 200:
        return

    with open(store_file_path, "wb+") as f:
        f.write(r.content)

    return store_file_path


def get_order_files_from_storage_unit(order: dict) -> None:
    assets = (
        "background_name",
        "foreground_name",
        "audio_name",
    )
    for asset in assets:
        asset_name = order.get(asset, None)
        if asset_name:
            get_file_from_storage_unit(asset_name)
