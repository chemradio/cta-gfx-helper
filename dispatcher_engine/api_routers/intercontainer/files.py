from enum import Enum

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from utils.assets.asset_finder import find_files

router = APIRouter()


class UploadFileCategory(str, Enum):
    SCREENSHOTS = "screenshots"
    VIDEO_EXPORTS = "video_exports"
    USER_FILES = "user_files"


class IntercontainerUploadFile(BaseModel):
    file: UploadFile
    category: UploadFileCategory

    class Config:
        use_enum_values = True


@router.get("/")
async def get_file(filename: str):
    search = find_files(filename)
    if not search:
        raise HTTPException(404, f"File *{filename}* not found")

    return FileResponse(search[0])


@router.post("/")
async def add_file(
    upload_file: UploadFile,
):
    file_category = upload_file.filename[0 : upload_file.filename.rindex("_")]

    with open(f"./volume/{file_category}/{upload_file.filename}", "wb") as f:
        f.write(upload_file.file.read())

    print(
        f"File {upload_file.filename} was stored under {file_category} category on the dispatcher node"
    )
    return {
        "detail": f"File {upload_file.filename} was stored under {file_category} category on the dispatcher node"
    }
