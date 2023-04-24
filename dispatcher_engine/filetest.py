from pathlib import Path
from typing import Optional

import requests


def post_file_to_dispatcher(file_path: Path | str) -> bool:
    """Post a file to the dispatcher node.
    The file category is appended to the beginning"""
    response = requests.post(
        "http://dispatcher",
        files={
            "upload_file": open(file_path, "rb"),
        },
    )
    if response.status_code != 200:
        return False
    return True
