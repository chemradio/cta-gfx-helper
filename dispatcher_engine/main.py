import asyncio
import os
import time

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

# from api_routers.administration import db_manipulation
from api_routers.helpers import text_processors

# from api_routers.intercontainer import files
from api_routers.intercontainer import orders as intercontainer_orders

# from api_routers.telegram_api import orders as telegram_orders
# from api_routers.telegram_api import users as telegram_users
from api_routers.universal import orders as universal_orders
from api_routers.universal import users as universal_users
from api_routers.user_files import user_file_handler

# from api_routers.web_api import direct_download
# from api_routers.web_api import orders as web_orders
# from api_routers.web_api import users as web_users
from create_volume_folders import create_volume_folders
from db_mongo.seeding.mandatory import seed_admin

# from db_tortoise.tort_config import TORTOISE_ORM
# from generate_schemas import main as db_check_rebuild
# from seeding import seed as seed_db
# from seeding import seed_admin

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
# app.include_router(db_manipulation.router, prefix="/admin/db_manipulation")

# web frontend
# app.include_router(web_orders.router, prefix="/web_api/orders")
# app.include_router(web_users.router, prefix="/web_api/users")
# app.include_router(direct_download.router, prefix="/web_api/direct_download")

# telegram frontend
# app.include_router(telegram_users.router, prefix="/telegram_api/users")
# app.include_router(telegram_orders.router, prefix="/telegram_api/orders")

# universal api
app.include_router(universal_users.router, prefix="/universal/users")
app.include_router(universal_orders.router, prefix="/universal/orders")

# user file receptor
app.include_router(user_file_handler.router, prefix="/user_files")

# intercontainer
app.include_router(intercontainer_orders.router, prefix="/intercontainer_orders")

# helpers
app.include_router(text_processors.router, prefix="/helpers/text_processor")


# app.include_router(validators.router, prefix="/validators")
# app.include_router(web_auth_local.router, prefix="/web_api/users")
# app.include_router(web_orders.router, prefix="/web_api/orders")
# app.include_router(temp_form.router)


def main():
    # seed admin
    seed_admin()
    print("Starting the server")
    config = uvicorn.Config(
        "main:app",
        port=os.environ.get("dispatcher_port", 9000),
        host="0.0.0.0" if os.environ.get("IS_DOCKER", True) else "127.0.0.1",
        log_level="info",
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    import time

    time.sleep(3)
    main()
    # uvicorn.run(
    #     app,
    #     host="0.0.0.0" if os.environ.get("IS_DOCKER", True) else "127.0.0.1",
    #     port=9000,
    # )
