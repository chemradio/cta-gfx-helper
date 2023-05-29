from pathlib import Path
from typing import Optional

from config import DEFAULT_PATH


def find_file(
    file_name: str,
    search_folders: list[Path] = [
        DEFAULT_PATH,
    ],
) -> list[Optional[Path]]:
    output = list()
    for folder in search_folders:
        if (folder / file_name).exists():
            output.append(folder / file_name)
    return output


def find_files(filenames: list[str]) -> list[Optional[Path]]:
    output_paths = list()

    for filename in filenames:
        if not filename:
            continue

        single_filename_paths = find_file(filename)
        if single_filename_paths:
            output_paths.extend(single_filename_paths)
    return output_paths
