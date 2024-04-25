import config
from pathlib import Path

def find_asset(filename: str, search_path: Path = config.SCREENSHOT_FOLDER) -> Path:
    return next(search_path.rglob(filename), None)

    