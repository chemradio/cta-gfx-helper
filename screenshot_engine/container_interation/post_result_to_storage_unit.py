import os
from pathlib import Path

import requests
from config import SCREENSHOT_FOLDER

STORAGE_UNIT_NAME = os.getenv("STORAGE_UNIT_NAME", "storage_unit")
STORAGE_UNIT_PORT = os.getenv("STORAGE_UNIT_PORT", 9010)
STORAGE_UNIT_ENDPOINT = f"http://{STORAGE_UNIT_NAME}:{STORAGE_UNIT_PORT}/file"


def store_result(order: dict):
    store_asset_list = (
        "background_name",
        "foreground_name",
    )
    search_folders = (SCREENSHOT_FOLDER,)

    # find assets
    output_paths = list()
    for asset in store_asset_list:
        asset_name = order.get(asset)
        for folder in search_folders:
            if (folder / str(asset_name)).exists():
                output_paths.append(folder / asset_name)
                break

    # store files to storage unit and erase locally
    for path in output_paths:
        store_file(path)
        # path.unlink()

    return


def store_file(filepath: str | Path) -> None:
    print("storing file:", filepath)
    response = requests.post(
        STORAGE_UNIT_ENDPOINT,
        files={"upload_file": open(filepath, "rb")},
        data={"category": "screenshots"},
    )
    assert response.status_code == 200
