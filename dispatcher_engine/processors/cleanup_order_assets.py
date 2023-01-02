from pathlib import Path
from typing import Optional

import config


def cleanup_order_assets(order: dict):
    bg_name = order.get("background_name")
    fg_name = order.get("foreground_name")
    audio_name = order.get("audio_name")
    video_gfx_name = order.get("video_gfx_name")
    paths = find_files(bg_name, fg_name, audio_name, video_gfx_name)
    if not paths:
        return

    for path in paths:
        path.unlink()

    html_assembly_name: str = order.get("html_assembly_name")
    if html_assembly_name:
        html_assembly_path = config.HTML_ASSEMBLIES_FOLDER / html_assembly_name
        if html_assembly_path.exists():
            remove_directory_recursively(html_assembly_path)


def find_files(*filenames: str) -> list[Optional[Path]]:
    paths = list()
    folders = (
        config.SCREENSHOTS_FOLDER,
        config.USER_FILES_FOLDER,
        config.RENDER_OUTPUT_PATH,
    )

    def find_file(file_name, search_folders) -> Optional[Path]:
        for folder in search_folders:
            if (folder / file_name).exists():
                return folder / file_name

    for filename in filenames:
        files_to_search = [filename]
        if "." in filename:
            files_to_search.append(filename.split(".")[0])

        for file in files_to_search:
            file_to_remove = find_file(file, folders)
            if file_to_remove:
                paths.append(file_to_remove)

    return paths


def remove_directory_recursively(path: Path):
    for item in path.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            remove_directory_recursively(item)
            item.rmdir()
    path.rmdir()
