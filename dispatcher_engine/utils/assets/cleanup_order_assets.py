from pathlib import Path

import config
from utils.assets.asset_finder import find_files


def cleanup_order_assets(order: dict):
    # get all possible db filenames
    bg_name: str = order.get("background_name")
    fg_name: str = order.get("foreground_name")
    audio_name: str = order.get("audio_name")
    video_gfx_name: str = order.get("video_gfx_name")
    html_assembly_name: str = order.get("html_assembly_name")

    # filter out missing filenames
    temp_filenames = (bg_name, fg_name, audio_name, video_gfx_name)
    order_filenames = (filename for filename in temp_filenames if filename)

    # add same filenames but without extensions - file type conversion artifacts
    target_filenames = list(order_filenames)
    dot_filenames = [filename for filename in target_filenames if "." in filename]

    for filename in dot_filenames:
        no_ext_filename = filename.split(".")[0]
        target_filenames.append(no_ext_filename)
        possible_extensions = (
            "pdf",
            "jpg",
            "jpeg",
            "wav",
            "mp3",
            "ogg",
        )
        target_filenames.extend(
            [f"{no_ext_filename}.{ext}" for ext in possible_extensions]
        )

    # find target file paths
    filepaths = find_files(*target_filenames)
    target_filepaths = (path for path in filepaths if path)

    # remove file paths
    if not target_filepaths:
        return None
    for filepath in target_filepaths:
        try:
            filepath.unlink()
        except:
            print(f"Failed to remove file: {filepath}")

    # remove html_assembly folder
    if html_assembly_name:
        html_path = config.HTML_ASSEMBLIES_FOLDER / html_assembly_name
        remove_tree(html_path)
        html_path.rmdir()


def remove_tree(path: Path) -> None:
    for item in path.glob("*"):
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            remove_tree(item)
            item.rmdir()
