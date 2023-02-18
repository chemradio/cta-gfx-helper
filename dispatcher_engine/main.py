from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from api_routers import (
    auth_local,
    db_backup_restore,
    direct_download,
    orders,
    temp_form,
    users,
    validators,
)
from create_volume_folders import create_volume_folders
from db.sql_handler import db

create_volume_folders()
db.recreate_tables()
db.init_add_admin()


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
app.include_router(auth_local.router, prefix="/auth_web_local")
app.include_router(temp_form.router)
app.include_router(direct_download.router)


# @app.get("/")
# async def read_root():
#     """Unused at the moment"""
#     with open("./base_html/index.html") as index_html:
#         data = index_html.read()
#     return Response(content=data, media_type="text/html")
