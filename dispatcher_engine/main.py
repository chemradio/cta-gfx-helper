import asyncio
import os
import time

import uvicorn
from api_routers.administration import db_manipulation
from api_routers.intercontainer import files
from api_routers.intercontainer import orders as intercontainer_orders
from api_routers.telegram_api import orders as telegram_orders
from api_routers.telegram_api import users as telegram_users
from api_routers.user_files import user_file_handler
from api_routers.web_api import direct_download
from api_routers.web_api import orders as web_orders
from api_routers.web_api import users as web_users
from create_volume_folders import create_volume_folders
from db_tortoise.tort_config import TORTOISE_ORM
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from generate_schemas import main as db_check_rebuild
from seeding import seed as seed_db
from seeding import seed_admin
from tortoise.contrib.fastapi import register_tortoise

create_volume_folders()

app = FastAPI()

origins = [
    "http://front_svelte",
    "http://localhost",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=1000000,
)


@app.get("/")
async def home(name: str):
    return f"Hello, {name}!"


# admin
app.include_router(db_manipulation.router, prefix="/admin/db_manipulation")

# web frontend
app.include_router(web_orders.router, prefix="/web_api/orders")
app.include_router(web_users.router, prefix="/web_api/users")
app.include_router(direct_download.router, prefix="/web_api/direct_download")

# telegram frontend
app.include_router(telegram_users.router, prefix="/telegram_api/users")
app.include_router(telegram_orders.router, prefix="/telegram_api/orders")

# user file receptor
app.include_router(user_file_handler.router, prefix="/user_files")

# intercontainer
app.include_router(intercontainer_orders.router, prefix="/intercontainer/orders")
app.include_router(files.router, prefix="/intercontainer/files")


# app.include_router(validators.router, prefix="/validators")
# app.include_router(web_auth_local.router, prefix="/web_api/users")
# app.include_router(web_orders.router, prefix="/web_api/orders")
# app.include_router(temp_form.router)

register_tortoise(
    app,
    db_url=TORTOISE_ORM["connections"]["default"],
    modules={
        "models": [
            "db_tortoise.users_models",
            "db_tortoise.orders_models",
            "db_tortoise.system_events_models",
        ]
    },
    add_exception_handlers=True,
)

from tortoise import Tortoise

Tortoise.init_models(
    ["db_tortoise.users_models", "db_tortoise.orders_models"], "models"
)


async def main():
    print("Dispatcher launch initiated")

    if os.environ.get("IS_DOCKER", True):
        print("Waiting 10 secs for DB check/rebuild")
        time.sleep(10)
    print("Running DB check / rebuild")
    await db_check_rebuild()
    print("DB check rebuild complete")

    if os.environ.get("IS_DOCKER", True):
        print("Seeding administrator")
        try:
            seed_result = await seed_db()
            print(f"Seeding admin done")
        except:
            print("failed to seed admin")

        print("Seeding if necessary")
        try:
            seed_result = await seed_db()
            print(f"Seeding done: {seed_result=}")
        except:
            print("failed to seed the db")

    print("Starting the server")
    config = uvicorn.Config(
        "main:app",
        port=os.environ.get("dispatcher_port", 9000),
        host="0.0.0.0" if os.environ.get("IS_DOCKER", True) else "127.0.0.1",
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
    # uvicorn.run(
    #     app,
    #     host="0.0.0.0" if os.environ.get("IS_DOCKER", True) else "127.0.0.1",
    #     port=9000,
    # )
