from pathlib import Path

import config


def gather_file_paths(order: dict) -> list:
    request_type = order.get("request_type")
    match request_type:
        case "video_auto":
            return gather_video_auto(order)
        case "video_files":
            return gather_video_files(order)
        case "only_screenshots":
            return gather_only_screenshots(order)
        case _:
            return []


def gather_video_auto(order: dict) -> list[Path]:
    video_gfx_name: str = order.get("video_gfx_name")
    video_gfx_path = config.VIDEO_GFX_FOLDER / str(video_gfx_name)
    if not video_gfx_path.exists():
        return None
    return [video_gfx_path]


def gather_video_files(order: dict) -> list[Path]:
    return gather_video_auto(order)


def gather_only_screenshots(order: dict) -> list[Path]:
    file_paths = list()
    for filename in ("background_name", "foreground_name"):
        screenshot_path = config.SCREENSHOTS_FOLDER / str(order[filename])
        if not screenshot_path.exists():
            continue
        file_paths.append(screenshot_path)
    return file_paths
