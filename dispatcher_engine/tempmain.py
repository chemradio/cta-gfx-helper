from fastapi import FastAPI

from api_routers import direct_download
from create_volume_folders import create_volume_folders

create_volume_folders()

app = FastAPI()
app.include_router(direct_download.router)
