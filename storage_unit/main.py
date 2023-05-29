import asyncio
import os
import threading

import uvicorn
from fastapi import FastAPI

from cleaner.cleanup_worker import expiry_asset_cleaner
from routers import receiver, transmitter


async def main():
    app = FastAPI()
    app.include_router(receiver.router)
    app.include_router(transmitter.router)

    config = uvicorn.Config(
        "main:app",
        port=os.environ.get("storage_unit_port", 9010),
        host="0.0.0.0" if os.environ.get("IS_DOCKER") else "127.0.0.1",
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    threading.Thread(target=expiry_asset_cleaner).start()
    asyncio.run(main())
