import shutil
from pathlib import Path


def remove_tree(path: Path) -> None:
    if path.exists():
        for item in path.glob("*"):
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
