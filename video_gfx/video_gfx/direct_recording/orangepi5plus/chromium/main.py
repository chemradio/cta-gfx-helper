import asyncio

import uvicorn
from fastapi import FastAPI, BackgroundTasks

from perform_test import perform_test

app = FastAPI()


@app.get("/start")
def start_test(bg_tasks: BackgroundTasks):
    bg_tasks.add_task(
        perform_test
    )


def main():
    config = uvicorn.Config(
        "main:app",
        port=9001,
        host="0.0.0.0",
        log_level="info",
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    main()
