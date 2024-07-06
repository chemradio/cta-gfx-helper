from fastapi import FastAPI

from .routers.file_server import router as file_server_router
from .routers.order_check import router as order_check_router

app = FastAPI()
app.include_router(file_server_router, prefix="/file_server")
app.include_router(order_check_router)
