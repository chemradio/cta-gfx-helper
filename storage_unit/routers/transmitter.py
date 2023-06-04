from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from utils.assets.asset_finder import find_file

router = APIRouter()


@router.get("/")
async def get_file(filename: str):
    search = find_file(filename)
    if not search:
        raise HTTPException(404, f"File *{filename}* not found")

    return FileResponse(search[0])
