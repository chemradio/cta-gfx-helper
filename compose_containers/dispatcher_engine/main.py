import asyncio
import os

import uvicorn
import api_routers
import api_routers.administration

# import api_routers.administration.admin_endpoints

from api_routers.universal.users import router as users_router
from api_routers.universal.orders import router as orders_router
from api_routers.helpers.text_processors import router as text_processors_router
from create_volume_folders import create_volume_folders
from db_mongo.seeding.mandatory import seed_admin
from db_mongo.seeding.optional import seed_users
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from api_routers.intercontainer import files
seed_admin()
seed_users()

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
# app.include_router(api_routers.administration.admin_endpoints.router, prefix="/admin")

# universal api
app.include_router(users_router, prefix="/users")
app.include_router(orders_router, prefix="/orders")


# helpers
app.include_router(text_processors_router, prefix="/helpers/text_processor")
