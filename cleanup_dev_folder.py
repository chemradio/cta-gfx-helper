from pathlib import Path

volume_path = Path.cwd() / "dev" / "volume"
assets_path = volume_path / "asset_storage"
asset_subpaths = (
    "cookie_file",
    "html_assemblies",
    "screenshots",
    "user_files",
    "video_exports",
)


def remove_tree(path: Path):
    for item in path.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            remove_tree(item)
            item.rmdir()


def main():
    for path in asset_subpaths:
        target_folder = assets_path / path
        remove_tree(target_folder)


if __name__ == "__main__":
    main()
