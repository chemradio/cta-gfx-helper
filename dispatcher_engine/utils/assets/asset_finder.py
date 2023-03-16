from pathlib import Path
from typing import Optional

import config


def find_files(*filenames: list[str]) -> list[Optional[Path]]:
    def find_file(file_name: str, search_folders: list[Path]) -> list[Optional[Path]]:
        output = list()
        for folder in search_folders:
            if (folder / file_name).exists():
                output.append(folder / file_name)
        return output

    def find_file_glob(
        file_name: str, search_folders: list[Path]
    ) -> list[Optional[Path]]:
        output = list()
        for folder in search_folders:
            glob_list = list(folder.glob(f"*{file_name}*"))
            if not glob_list:
                continue
            for item in glob_list:
                if item.exists():
                    output.append(folder / file_name)
        return output

    output_paths = list()
    folders = (
        config.SCREENSHOTS_FOLDER,
        config.USER_FILES_FOLDER,
        config.RENDER_OUTPUT_PATH,
    )

    for filename in filenames:
        if not filename:
            continue

        files_to_remove = find_file(filename, folders)
        if files_to_remove:
            output_paths.extend(files_to_remove)
    return output_paths
