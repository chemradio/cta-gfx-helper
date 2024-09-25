from pathlib import Path


def remove_tree(path: Path) -> None:
    for item in path.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            remove_tree(item)
            item.rmdir()
    path.rmdir()
