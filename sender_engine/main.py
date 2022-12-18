from pathlib import Path

from fastapi import BackgroundTasks, FastAPI

from send_process.orders_sender import orders_sender


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


@app.post("/send_orders")
async def send_orders(background_tasks: BackgroundTasks):
    background_tasks.add_task(orders_sender)
    return True
