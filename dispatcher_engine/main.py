import asyncio
import os

import uvicorn
from api_routers.helpers import text_processors
from api_routers.universal import orders as universal_orders
from api_routers.universal import users as universal_users
from create_volume_folders import create_volume_folders
from db_mongo.seeding.mandatory import seed_admin
from db_mongo.seeding.optional import seed_users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from api_routers.intercontainer import files


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

# universal api
app.include_router(universal_users.router, prefix="/universal/users")
app.include_router(universal_orders.router, prefix="/universal/orders")


# helpers
app.include_router(text_processors.router, prefix="/helpers/text_processor")


def main():
    # seed admin and users
    seed_admin()
    seed_users()

    print("Starting the server")
    config = uvicorn.Config(
        "main:app",
        port=os.environ.get("dispatcher_port", 9000),
        host="0.0.0.0" if os.environ.get("IS_DOCKER", True) else "127.0.0.1",
        log_level="info",
        reload=True,
    )
    server = uvicorn.Server(config)
    asyncio.run(server.serve())
