import asyncio

import uvicorn

from fastapi import FastAPI, BackgroundTasks
from recording import perform_recording

app = FastAPI()


@app.get("/record")
def record(bg_tasks: BackgroundTasks):
    bg_tasks.add_task(perform_recording)


def main():
    config = uvicorn.Config(
        "main:app",
        port=9002,
        host="0.0.0.0",
        log_level="info",
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    import time

    time.sleep(3)
    main()
