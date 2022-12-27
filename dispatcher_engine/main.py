from db.sql_handler import db
from fastapi import FastAPI
from api_routers import cookie_file, db_backup_restore, orders, users
from create_volume_folders import create_volume_folders

create_volume_folders()
db.recreate_tables()
db.init_add_admin()

app = FastAPI()
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(cookie_file)
app.include_router(db_backup_restore.router)


@app.get("/")
async def read_root():
    """Unused at the moment"""
    return {"Hello": "World"}
