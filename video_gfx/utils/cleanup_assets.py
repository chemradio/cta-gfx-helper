from pathlib import Path

from config import (
    HTML_ASSEMBLIES_FOLDER,
    RENDER_OUTPUT_PATH,
    SCREENSHOTS_FOLDER,
    USER_FILES_FOLDER,
)


def cleanup_order(order: dict) -> None:
    store_asset_list = (
        "video_gfx_name",
        "background_name",
        "foreground_name",
    )
    search_folders = (RENDER_OUTPUT_PATH, SCREENSHOTS_FOLDER, USER_FILES_FOLDER)

    # find assets
    for asset in store_asset_list:
        asset_name = order.get(asset)
        for folder in search_folders:
            if (folder / asset_name).exists():
                (folder / asset_name).unlink()
                continue

    # cleanup html assembly
    html_assembly_name = order.get("html_assembly_name")
    html_assembly_folder_path = HTML_ASSEMBLIES_FOLDER / html_assembly_name
    if html_assembly_folder_path.exists():
        remove_tree(html_assembly_folder_path)
    return


def remove_tree(path: Path) -> None:
    for item in path.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            remove_tree(item)
            item.rmdir()
    path.rmdir()
