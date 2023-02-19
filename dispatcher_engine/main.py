from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_routers import (
    db_backup_restore,
    direct_download,
    orders,
    temp_form,
    users,
    validators,
)
from api_routers.web_api import web_auth_local, web_orders
from create_volume_folders import create_volume_folders
from db.seeding import seed_db

create_volume_folders()
seed_db()

app = FastAPI()

origins = origins = [
    # "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users.router, prefix="/users")
app.include_router(orders.router, prefix="/orders")
app.include_router(db_backup_restore.router, prefix="/database")
app.include_router(validators.router, prefix="/validators")
app.include_router(web_auth_local.router, prefix="/web_api/users")
app.include_router(web_orders.router, prefix="/web_api/orders")
app.include_router(temp_form.router)
app.include_router(direct_download.router)
