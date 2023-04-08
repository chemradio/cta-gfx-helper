import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from api_routers.administration import db_manipulation
from api_routers.intercontainer import orders as intercontainer_orders
from api_routers.web_api import direct_download
from api_routers.web_api import orders as web_orders
from api_routers.web_api import users as web_users
from create_volume_folders import create_volume_folders
from db_tortoise.init_tort_orm import (
    initialize_tortoise_postgres,
    rebuild_tortoise_postgres,
)
from db_tortoise.tort_config import TORTOISE_ORM

asyncio.get_event_loop().create_task(initialize_tortoise_postgres())

create_volume_folders()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:5176",
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

# intercontainer
app.include_router(intercontainer_orders.router, prefix="/intercontainer/orders")


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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
