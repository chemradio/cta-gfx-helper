import secrets
import time


def generate_filenames() -> tuple[str, str, str]:
    background_name = f"01_BG_{secrets.token_hex(8)}.png"
    foreground_name = f"02_FG_{secrets.token_hex(8)}.png"
    video_gfx_name = f"video-auto-gfx-{int(time.time())}.mp4"
    return background_name, foreground_name, video_gfx_name


def assign_filenames(order: dict) -> dict:
    request_type = order.get("request_type")
    background_name, foreground_name, video_gfx_name = generate_filenames()

    match request_type:
        case "video_auto":
            order["background_name"] = background_name
            order["foreground_name"] = foreground_name
            order["video_gfx_name"] = video_gfx_name
        case "video_files":
            order["video_gfx_name"] = video_gfx_name
        case "only_screenshots":
            order["background_name"] = background_name
            order["foreground_name"] = foreground_name
        case _:
            return None

    return order
