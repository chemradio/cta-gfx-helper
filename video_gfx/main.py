from pathlib import Path

from fastapi import FastAPI

from video_gfx.order_processor import video_gfx_thread


def create_volume_folders():
    volume_path = Path().cwd() / "volume"

    children = (
        "cookie_file",
        "html_assemblies",
        "screenshots",
        "user_files",
        "video_exports",
    )
    children_paths = [volume_path / child for child in children]
    for child_path in children_paths:
        child_path.mkdir(parents=True, exist_ok=True)


create_volume_folders()

app = FastAPI()


@app.post("/start_video_gfx")
def start_video_gfx():
    video_gfx_thread()
    return True
