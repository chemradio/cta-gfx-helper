import asyncio
import os

import uvicorn
import api_routers
import api_routers.administration
import api_routers.administration.admin_endpoints
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
app.include_router(api_routers.administration.admin_endpoints.router, prefix="/admin")

# universal api
app.include_router(api_routers.universal.users.router, prefix="/users")
app.include_router(api_routers.universal.orders.router, prefix="/orders")


# helpers
app.include_router(
    api_routers.helpers.text_processors.router, prefix="/helpers/text_processor"
)


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