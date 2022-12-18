from pathlib import Path

from fastapi import BackgroundTasks, FastAPI

from screenshots.screenshot_order_processor import process_screenshot_orders


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


@app.post("/start_screenshoting")
async def start_screenshooting(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_screenshot_orders)
    return True
