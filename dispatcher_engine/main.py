from api_routers import db_backup_restore, orders, temp_form, users, validators
from create_volume_folders import create_volume_folders
from db.sql_handler import db
from fastapi import FastAPI, Response

create_volume_folders()
db.recreate_tables()
db.init_add_admin()

app = FastAPI()
app.include_router(users.router, prefix="/users")
app.include_router(orders.router, prefix="/orders")
app.include_router(db_backup_restore.router, prefix="/database")
app.include_router(validators.router, prefix="/validators")
app.include_router(temp_form.router)


# @app.get("/")
# async def read_root():
#     """Unused at the moment"""
#     with open("./base_html/index.html") as index_html:
#         data = index_html.read()
#     return Response(content=data, media_type="text/html")
