import asyncio
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from video_gfx.order_processor import video_gfx_thread

volume_path = Path().cwd() / "volume"


def create_volume_folders():
    children = (
        "cookie_file",
        "html_assemblies",
        "screenshots",
        "user_files",
        "video_exports",
        "from_storage_unit",
    )
    children_paths = [volume_path / child for child in children]
    for child_path in children_paths:
        child_path.mkdir(parents=True, exist_ok=True)


create_volume_folders()

app = FastAPI()

html_assemblies_path = volume_path / "html_assemblies"
app.mount(
    "/html_assemblies/",
    StaticFiles(directory=html_assemblies_path.resolve()),
    name="static",
)


@app.post("/start_video_gfx")
async def start_video_gfx():
    video_gfx_thread()
    return True


async def main():
    config = uvicorn.Config(
        "main:app",
        port=int(os.environ.get("video_gfx_port", 9004)),
        host="0.0.0.0",
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())


# @app.get("/video_gfx_server/{html_assembly_name}")
# async def serve_html_assembly(html_assembly_name: str):
#     return "ok"
