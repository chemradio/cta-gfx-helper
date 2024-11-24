import shutil
from pathlib import Path


def purge_storage(storage_path: Path) -> None:
    if storage_path.exists():
        for file in storage_path.rglob("*"):
            if file.is_file():
                file.unlink()
            elif file.is_dir():
                shutil.rmtree(file)
    else:
        storage_path.mkdir()
