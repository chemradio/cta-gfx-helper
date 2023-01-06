from api_routers import db_backup_restore, orders, users
from create_volume_folders import create_volume_folders
from db.sql_handler import db
from fastapi import FastAPI

create_volume_folders()
db.recreate_tables()
db.init_add_admin()

app = FastAPI()
app.include_router(users.router, prefix="/users")
app.include_router(orders.router, prefix="/orders")
app.include_router(db_backup_restore.router, prefix="/database")


@app.get("/")
async def read_root():
    """Unused at the moment"""
    return {"Hello": "World"}
